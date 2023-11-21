import math
from typing import Optional
from pathlib import Path
import os
from functools import partial
from llama_index.llms import OpenAI
from llama_index import ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.retrievers import KnowledgeGraphRAGRetriever
from llama_index.query_engine import RetrieverQueryEngine
from ai2thor.server import MetadataWrapper
from knowledge_graph.update_graph import process_state_change
from knowledge_graph.age_graph import AgeGraphStore
from knowledge_graph.utils import get_prompt_template, extract_keywords
from contextlib import redirect_stdout
import time
import random

TIME_LIMIT = 100


class KnowledgeGraphThorAgent:

    def __init__(self,
                 controller,
                 host: str,
                 dbname: str,
                 user: str,
                 password: str,
                 port: Optional[int] = 5432,
                 graph_name: Optional[str] = "knowledge_graph",
                 log_dir: Optional[str] = ""):
        self._controller = controller
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
        self._service_context = ServiceContext.from_defaults(llm=self._llm)
        self._storage_context = StorageContext.from_defaults(graph_store=self._graph_store)
        self._rag_update_retriever = KnowledgeGraphRAGRetriever(
            storage_context=self._storage_context,
            service_context=self._service_context,
            verbose=True,
            graph_traversal_depth=1,
            max_knowledge_sequence=200,
            entity_extract_fn=partial(extract_keywords, self._graph_store, self._service_context,
                                      get_prompt_template("entity_select_prompt.txt")),
            entity_extract_policy="union"
        )

        self._domain_file = "planning/domain.pddl"
        domain_file_path = Path(__file__).parent.parent / self._domain_file
        with open(domain_file_path, "r") as f:
            self._domain_pddl = f.read()
        template = get_prompt_template("plan_entity_select_prompt.txt")
        template = template.replace('domain_pddl', self._domain_pddl)
        self._rag_plan_retriever = KnowledgeGraphRAGRetriever(
            storage_context=self._storage_context,
            service_context=self._service_context,
            verbose=True,
            graph_traversal_depth=2,
            max_knowledge_sequence=500,
            max_entities=10,
            entity_extract_fn=partial(extract_keywords, self._graph_store, self._service_context, template),
            entity_extract_policy="union"
        )
        self._query_engine = RetrieverQueryEngine.from_args(
            self._rag_plan_retriever, service_context=self._service_context
        )

        self._log_dir = log_dir
        self._change_count = 0
        self._query_count = 0
        self._name_to_id = {}
        self._static_locations = []

    def input_initial_state(self, initial_state: str, knowledge_yaml: str) -> None:
        pass



    def load_relation(self, obj, r, metadata, cur):

        if r == 'receptacleObjectIds':
            self._graph_store.delete_rel_with_obj('isPlacedAt', obj['name'])
            if obj[r] is None:
                return
            elif len(obj[r]) == 1:
                self._graph_store.upsert_triplet_entity(obj[r][0], 'isPlacedAt', obj['objectId'])
            else:
                for v in obj[r]:
                    v_obj = [o for o in metadata['objects'] if o['objectId'] == v][0]
                    intermediate_receptacles = [o for o in v_obj['parentReceptacles'] if o in obj[r]]
                    if len(intermediate_receptacles) > 0:
                        continue
                    self._graph_store.upsert_triplet_entity(v, 'isPlacedAt', obj['objectId'])
        elif r == 'objectType':
            if obj[r] in ['SinkBasin', 'Microwave', 'Fridge']:
                self._graph_store.upsert_triplet_bool(obj['objectId'], 'is' + obj[r], True)
        else:
            self._graph_store.delete_rel_with_subj(obj['name'], r)
            if type(obj[r]) == list:
                for v in obj[r]:
                    self._graph_store.upsert_triplet_entity(obj['objectId'], r, v)
            elif type(obj[r]) == bool:
                self._graph_store.upsert_triplet_bool(obj['objectId'], r, obj[r])
            elif type(obj[r]) == float:
                self._graph_store.upsert_triplet_float(obj['objectId'], r, obj[r])
            elif type(obj[r]) == str:
                self._graph_store.upsert_triplet_str(obj['objectId'], r, obj[r])
            elif obj[r] is None:
                self._graph_store.upsert_triplet_str(obj['objectId'], r, 'None')


    def load_simulation_state(self, metadata: MetadataWrapper) -> None:
        for obj in metadata['objects']:
            if not obj['pickupable'] and obj['receptacle']:
                self._static_locations.append(obj['name'])
            self._name_to_id[obj['name']] = obj['objectId']

        cur = self._graph_store.cursor()
        cur.execute(f"SELECT * FROM ag_catalog.drop_graph('{self.graph_name}', true)")
        cur.execute(f"SELECT * FROM ag_catalog.create_graph('{self.graph_name}')")
        cur.execute(f"SELECT * FROM ag_catalog.create_vlabel('{self.graph_name}', 'entity');")
        closest_interactable_object = None
        closest_interactable_distance = math.inf

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
                      'pickupable': ['isPickedUp'],
                      'objectType': []}
        # 'moveable': ['isMoving']}

        # general_properties = ['visible', 'isInteractable', 'temperature', 'mass', 'controlledObjects']
        general_properties = ['temperature', 'controlledObjects']

        for obj in metadata['objects']:

            if obj['objectType'] == 'Floor':
                continue

            # set_property_query = ", ".join([f"a.{p}='{obj[p]}'" for p in properties.keys()])
            cur.execute(
                f"SELECT * FROM cypher('{self.graph_name}', "
                f"$$MERGE (a:entity {{id: '{obj['objectId']}'}}) "
                f"SET a.name='{obj['name']}'"
                f"RETURN a $$) as (a agtype);")

            for p in properties.keys():
                if obj[p]:
                    self.load_relation(obj, p, metadata, cur)
                    for relation in properties[p]:
                        self.load_relation(obj, relation, metadata, cur)

            for p in general_properties:
                self.load_relation(obj, p, metadata, cur)

            if obj['isInteractable'] and obj['distance'] < closest_interactable_distance:
                closest_interactable_object = obj
                closest_interactable_distance = obj['distance']

        # Create the robot node
        cur.execute(
            f"SELECT * FROM cypher('{self.graph_name}', "
            f"$$MERGE (a:entity {{id: '{metadata['agent']['name']}'}}) "
            f"SET a.name='Robot'"
            f"RETURN a $$) as (a agtype);")

        if closest_interactable_object:
            cur.execute(
                f"SELECT * FROM cypher('{self.graph_name}', $$MATCH (u:entity {{id: '{metadata['agent']['name']}'}}), "
                f"(v:entity {{id: '{closest_interactable_object['objectId']}'}}) "
                f"CREATE (u)-[e:atLocation]->(v) RETURN e$$) as (e agtype);")
            self._current_location = closest_interactable_object['name']

        if len(metadata['inventoryObjects']) > 0:
            self._graph_store.upsert_triplet_entity(metadata['agent']['name'], 'isHolding', metadata['inventoryObjects'][0]['objectId'])

    def go_to_object(self, object_name):
        object_id = self._name_to_id[object_name]
        event = self._controller.step(action='PositionsFromWhichItemIsInteractable', objectId=object_id)
        poses = event.metadata['actionReturn']
        for i in range(len(poses['x'])):
            position = dict(x=poses['x'][i], y=poses['y'][i], z=poses['z'][i])
            event = self._controller.step(action="TeleportFull",
                                          position=position,
                                          rotation=dict(y=poses['rotation'][i]),
                                          standing=poses['standing'][i], horizon=poses['horizon'][i])
            if event.metadata['lastActionSuccess']:
                obj = [o for o in event.metadata['objects'] if o['name'] == object_name][0]
                if obj['isInteractable'] and obj['visible']:
                    self.input_observed_state()
                    return True

        return False

    def open_object(self, object_name):
        object_id = self._name_to_id[object_name]
        event = self._controller.step(action='OpenObject', objectId=object_id, forceAction=True)
        self.input_observed_state()
        return event.metadata['lastActionSuccess']

    def close_object(self, object_name):
        object_id = self._name_to_id[object_name]
        event = self._controller.step(action='CloseObject', objectId=object_id, forceAction=True)
        self.input_observed_state()
        return event.metadata['lastActionSuccess']

    def input_observed_state(self):
        observable_properties = {'receptacle': ['receptacleObjectIds'],
                                 'breakable': ['isBroken'],
                                 'canFillWithLiquid': ['isFilledWithLiquid', 'fillLiquid'],
                                 'dirtyable': ['isDirty'],
                                 'canBeUsedUp': ['isUsedUp'],
                                 'sliceable': ['isSliced'],
                                 'openable': ['isOpen', 'openness'],
                                 'pickupable': ['isPickedUp']}
        event = self._controller.step(action='GetVisibleObjects')
        visible_object_ids = event.metadata['actionReturn']
        cur = self._graph_store.cursor()
        for id in visible_object_ids:
            visible_obj = [o for o in event.metadata['objects'] if o['objectId'] == id][0]
            self._name_to_id[visible_obj['name']] = visible_obj['objectId']
            if visible_obj['objectType'] == 'Floor':
                continue
            cur.execute(
                f"SELECT * FROM cypher('{self.graph_name}', "
                f"$$MERGE (a:entity {{id: '{visible_obj['objectId']}'}}) "
                f"SET a.name='{visible_obj['name']}'"
                f"RETURN a $$) as (a agtype);")
            for p in observable_properties.keys():
                if visible_obj[p]:
                    for relation in observable_properties[p]:
                        self.load_relation(visible_obj, relation, event.metadata, cur)
        self._graph_store.delete_rel_with_subj(event.metadata['agent']['name'], 'isHolding')
        if len(event.metadata['inventoryObjects']) > 0:
            self._graph_store.upsert_triplet_entity(event.metadata['agent']['name'], 'isHolding',
                                                    event.metadata['inventoryObjects'][0]['objectId'])


    def wander(self) -> None:
        next_location = random.choice(self._static_locations)
        while next_location == self._current_location:
            next_location = random.choice(self._static_locations)
        self.go_to_object(next_location)
        object_states = self._controller.last_event.metadata['objects']
        obj = [o for o in object_states if o['name'] == next_location][0]
        if obj['openable']:
            self.open_object(next_location)
        for contained_id in obj['receptacleObjectIds']:
            contained_obj = [o for o in object_states if o['objectId'] ==    contained_id][0]
            self.go_to_object(contained_obj['name'])
        if obj['openable']:
            self.close_object(next_location)
        return

    def input_state_change(self, state_change: str) -> None:
        results_file = self._log_dir + "/text_update_" + str(self._change_count) + ".log"
        process_state_change(self._rag_update_retriever, self._graph_store, self._llm, state_change, results_file)
        self._change_count += 1

    def answer_planning_query(self, query: str) -> None:
        # A. generate problem pddl file
        log_file = self._log_dir + "/plan_query_" + str(self._query_count) + ".log"

        with open(log_file + ".context.log", "w") as f:
            f.write(query + "\n")
            with redirect_stdout(f):
                nodes = self._query_engine.retrieve("I have a task for the robot: " + query)

        objects = set()
        constants = {'Cold', 'Hot', 'RoomTemp', 'Water', 'Coffee', 'Wine'}
        init_block = "\t(:init\n"
        for rel in nodes[0].metadata['kg_rel_text']:
            predicate = rel.split('-[')[1].split(']')[0]
            arg1 = rel.split(',')[0]
            arg2 = rel.split('-> ')[1]
            if arg2 == 'True':
                init_block += f"\t\t({predicate} {arg1})\n"
                if arg1 != "Robot":
                    objects.add(arg1)
            elif arg2 == 'None' or arg2 == 'False':
                continue
            else:
                init_block += f"\t\t({predicate} {arg1} {arg2})\n"
                if arg1 != "Robot":
                    objects.add(arg1)
                if arg2 not in constants:
                    objects.add(arg2)
        init_block += "\t)\n"
        objects_block = "\t(:objects\n" + \
                        "\t\tRobot - robot\n"
        for obj in objects:
            objects_block += f"\t\t{obj} - object\n"
        objects_block += "\t)\n"

        plan_query_prompt = get_prompt_template("plan_query_prompt.txt").format(domain_pddl=self._domain_pddl,
                                                                                task_nl=query)
        goal_block = self._query_engine._response_synthesizer.synthesize(query=plan_query_prompt, nodes=nodes).response

        task_pddl_ = f"(define (problem p{self._query_count})\n" + \
                     f"\t(:domain robot)\n" + \
                     objects_block + \
                     init_block + \
                     f"\t{goal_block}\n)"

        # B. write the problem file into the problem folder
        task_pddl_file_name = self._log_dir + "/problem_" + str(self._query_count) + ".pddl"
        with open(task_pddl_file_name, "w") as f:
            f.write(task_pddl_)
        time.sleep(1)

        # C. run lapkt to plan
        plan_file_name = self._log_dir + "/plan_" + str(self._query_count) + ".pddl"

        project_dir = Path(__file__).parent.parent.as_posix()
        os.system(f"docker run -v {project_dir}:/root/experiments lapkt/lapkt-public ./siw-then-bfsf " + \
                  f"--domain /root/experiments/{self._domain_file} " + \
                  f"--problem /root/experiments/{task_pddl_file_name} " + \
                  f"--output /root/experiments/{plan_file_name} " + \
                  f"> {log_file}.pddl.log")

        self._query_count += 1

    def answer_query(self, query: str) -> str:
        pass
