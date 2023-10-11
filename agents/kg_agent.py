from typing import Optional
from pathlib import Path
import os
from functools import partial
from llama_index.llms import OpenAI
from llama_index import ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.retrievers import KnowledgeGraphRAGRetriever
from ai2thor.server import MetadataWrapper
from knowledge_graph.update_graph import process_state_change
from knowledge_graph.age_graph import AgeGraphStore
from knowledge_graph.utils import get_prompt_template, extract_keywords

class KnowledgeGraphThorAgent:

    def __init__(self,
                 host: str,
                 dbname: str,
                 user: str,
                 password: str,
                 port: Optional[int] = 5432,
                 graph_name: Optional[str] = "knowledge_graph",
                 log_dir: Optional[str] = ""):
        self.graph_name = graph_name
        self._graph_store = AgeGraphStore(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            graph_name=graph_name,
            node_label="entity"
        )
        # set API key
        openai_keys_file = Path(__file__).parent.parent / "keys" / "openai_keys.txt"
        with open(openai_keys_file.as_posix(), "r") as f:
            keys = f.read()
        keys = keys.strip().split('\n')
        os.environ["OPENAI_API_KEY"] = keys[0]
        self._llm = OpenAI(temperature=0, model="gpt-4")

        # self._updater = KnowledgeGraphUpdater(llm=llm, graph_store=self._graph_store)
        self._service_context = ServiceContext.from_defaults(llm=self._llm)
        self._storage_context = StorageContext.from_defaults(graph_store=self._graph_store)
        self._graph_rag_retriever = KnowledgeGraphRAGRetriever(
            storage_context=self._storage_context,
            service_context=self._service_context,
            verbose=True,
            graph_traversal_depth=1,
            max_knowledge_sequence=200,
            entity_extract_fn=partial(extract_keywords, self._graph_store, self._service_context),
            entity_extract_policy="union"
        )

        self._log_dir = log_dir
        self._change_count = 0
        self._query_count = 0

    def input_initial_state(self, initial_state: str, knowledge_yaml: str) -> None:
        pass

    def load_simulation_state(self, metadata: MetadataWrapper) -> None:
        cur = self._graph_store.cursor()
        cur.execute(f"SELECT * FROM ag_catalog.drop_graph('{self.graph_name}', true)")
        cur.execute(f"SELECT * FROM ag_catalog.create_graph('{self.graph_name}')")
        cur.execute(f"SELECT * FROM ag_catalog.create_vlabel('{self.graph_name}', 'entity');")

        properties = {'receptacle': ['receptacleObjectIds'],
                      'toggleable': ['isToggled'],
                      'breakable': ['isBroken'],
                      'canFillWithLiquid': ['isFilledWithLiquid', 'fillLiquid'],
                      'dirtyable': ['isDirty'],
                      'canBeUsedUp': ['isUsedUp'],
                      'cookable': ['isCooked'],
                      'isHeatSource': [],
                      'isColdSource': [],
                      'sliceable': ['isSliced'],
                      'openable': ['isOpen', 'openness'],
                      'pickupable': ['isPickedUp']}
                      # 'moveable': ['isMoving']}

        general_properties = ['visible', 'temperature', 'mass', 'controlledObjects']

        for obj in metadata['objects']:

            if obj['objectType'] == 'Floor':
                continue

            set_property_query = ", ".join([f"a.{p}='{obj[p]}'" for p in properties.keys()])
            cur.execute(
                f"SELECT * FROM cypher('{self.graph_name}', "
                f"$$MERGE (a:entity {{id: '{obj['objectId']}'}}) "
                f"SET a.name='{obj['name']}', a.type='{obj['objectType']}', {set_property_query} "
                f"RETURN a $$) as (a agtype);")

            def load_relation(r):
                if type(obj[r]) == list:
                    for v in obj[r]:
                        cur.execute(
                            f"SELECT * FROM cypher('{self.graph_name}', "
                            f"$$MERGE (a:entity {{id: '{v}' }}) "
                            f"RETURN a $$) as (a agtype);")
                        if r == 'receptacleObjectIds':
                            cur.execute(
                                f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{obj['objectId']}'}}), "
                                f"(v:entity {{id: '{v}'}}) CREATE (v)-[e:isPlacedAt]->(u) RETURN e$$) as (e agtype);")
                        else:
                            cur.execute(
                                f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{obj['objectId']}'}}), "
                                f"(v:entity {{id: '{v}'}}) CREATE (u)-[e:{r}]->(v) RETURN e$$) as (e agtype);")
                elif type(obj[r]) == bool:
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', "
                        f"$$MERGE (a:bool {{name: '{obj[r]}' }}) "
                        f"RETURN a $$) as (a agtype);")
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{obj['objectId']}'}}), "
                        f"(v:bool {{name: '{obj[r]}'}}) CREATE (u)-[e:{r}]->(v) RETURN e$$) as (e agtype);")
                elif type(obj[r]) == float:
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', "
                        f"$$MERGE (a:float {{name: '{obj[r]}' }}) "
                        f"RETURN a $$) as (a agtype);")
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{obj['objectId']}'}}), "
                        f"(v:float {{name: '{obj[r]}'}}) CREATE (u)-[e:{r}]->(v) RETURN e$$) as (e agtype);")
                elif type(obj[r]) == str:
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', "
                        f"$$MERGE (a:str {{name: '{obj[r]}' }}) "
                        f"RETURN a $$) as (a agtype);")
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{obj['objectId']}'}}), "
                        f"(v:str {{name: '{obj[r]}'}}) CREATE (u)-[e:{r}]->(v) RETURN e$$) as (e agtype);")
                elif obj[r] is None:
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', "
                        f"$$MERGE (a:str {{name: 'None' }}) "
                        f"RETURN a $$) as (a agtype);")
                    cur.execute(
                        f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{obj['objectId']}'}}), "
                        f"(v:str {{name: 'None'}}) CREATE (u)-[e:{r}]->(v) RETURN e$$) as (e agtype);")

            for p in properties.keys():
                if obj[p]:
                    for relation in properties[p]:
                        load_relation(relation)

            for p in general_properties:
                load_relation(p)

    def input_state_change(self, state_change: str) -> None:
        results_file = self._log_dir + "/text_update_" + str(self._change_count) + ".log"
        process_state_change(self._graph_rag_retriever, self._graph_store, self._llm, state_change, results_file)
        self._change_count += 1

    def answer_planning_query(self, query: str) -> None:
        pass

    def answer_query(self, query: str) -> str:
        pass
