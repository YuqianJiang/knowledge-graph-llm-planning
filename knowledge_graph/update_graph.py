import os
import logging
import sys
from typing import Optional
from llama_index.llms.utils import LLMType
from llama_index.graph_stores.types import GraphStore
from llama_index.indices.keyword_table.utils import extract_keywords_given_response
from llama_index.prompts import PromptTemplate, PromptType
from llama_index import PromptTemplate, ServiceContext
from llama_index.storage.storage_context import StorageContext
from llama_index.llms import OpenAI
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import KnowledgeGraphRAGRetriever
import re

# read prompt template from file and format
def get_prompt_template(filename: str, **kwargs) -> str:
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        contents = f.read()
    if not kwargs:
        return contents
    return contents.format(**kwargs)

TRIPLET_FILTER_PROMPT = get_prompt_template("triplet_filter_prompt.txt")
TRIPLET_UPDATE_PROMPT = get_prompt_template("triplet_update_prompt.txt")



class KnowledgeGraphUpdater():
    def __init__(self,
                 llm: LLMType,
                 graph_store: GraphStore):
        self._llm = llm
        self._service_context = ServiceContext.from_defaults(llm=llm)
        self._storage_context = StorageContext.from_defaults(graph_store=graph_store)
        self._graph_rag_retriever = KnowledgeGraphRAGRetriever(
            storage_context=self._storage_context,
            service_context=self._service_context,
            verbose=True,
            graph_traversal_depth=1,
            max_knowledge_sequence=200
            # entity_extract_fn=self.extract_keywords
        )
        self._graph_store = graph_store

    def extract_keywords(self, query_str: str,
                         max_keywords: Optional[int] = 5,
                         result_start_token: Optional[str] = "KEYWORDS:"):
        entities = self._graph_store.query("MATCH (V:entity) RETURN V.name")
        entity_names = ", ".join([e[0].strip('\"') for e in entities])

        # load in all default prompts
        ENTITY_SELECT_TEMPLATE = get_prompt_template("entity_select_prompt.txt", entity_names=entity_names)
        ENTITY_SELECT_PROMPT = PromptTemplate(
            ENTITY_SELECT_TEMPLATE,
            prompt_type=PromptType.QUERY_KEYWORD_EXTRACT,
        )
        response = self._service_context.llm_predictor.predict(
            ENTITY_SELECT_PROMPT,
            max_keywords=max_keywords,
            question=query_str,
        )
        extracted_entities = extract_keywords_given_response(
            response, start_token=result_start_token, lowercase=False
        )
        return extracted_entities

    def process_state_change(self, state_change: str, out_file_name: str) -> None:
        output = "------------------------------------------------\n"
        output += f"STATE CHANGE: {state_change}\n"

        entities = self._graph_store.query("MATCH (V:entity) RETURN V.name")
        entity_names = ", ".join([e[0].strip('\"') for e in entities])

        # load in all default prompts
        ENTITY_SELECT_TEMPLATE = get_prompt_template("entity_select_prompt.txt", entity_names=entity_names)
        ENTITY_SELECT_PROMPT = PromptTemplate(
            ENTITY_SELECT_TEMPLATE,
            prompt_type=PromptType.QUERY_KEYWORD_EXTRACT,
        )

        self._graph_rag_retriever._entity_extract_template = ENTITY_SELECT_PROMPT

        # retrieve relevant triplets with llama-index (but prevent llama-index printing)
        with open(os.devnull,"w") as devNull:
            orig = sys.stdout
            sys.stdout = devNull
            context_nodes = self._graph_rag_retriever.retrieve(state_change)
            sys.stdout = orig
        context_str = context_nodes[0].text if len(context_nodes) > 0 else "None"

        # format triplets from AGE query output
        def postprocess_triplet(triplet: str) -> str:
            components = [re.sub(r'[^a-zA-Z0-9_.]', '', component) for component in triplet.split(", ")]
            return " -> ".join(components)

        triplets = [postprocess_triplet(triplet) for triplet in context_str.split('\n')[2:]]
        triplet_str = '\n'.join(triplets)

        output += "------------------------------------------------\n"
        output += "EXTRACTED TRIPLETS:\n\n"
        output += triplet_str + "\n"

        # filter out irrelevant triplets using LLM directly
        filtered_triplet_str = self._llm.complete(TRIPLET_FILTER_PROMPT.format(state_change=state_change, triplet_str=triplet_str)).text
        output += "------------------------------------------------\n"
        output += "FILTERED TRIPLETS:\n\n"
        output += filtered_triplet_str + "\n"

        # query LLM to update triplets (remove existing and add new)
        triplet_updates = self._llm.complete(TRIPLET_UPDATE_PROMPT.format(state_change=state_change, filtered_triplet_str=filtered_triplet_str)).text
        output += "------------------------------------------------\n"
        output += "TRIPLETS TO ADD AND REMOVE\n\n"
        output += triplet_updates + "\n"
        output += "------------------------------------------------\n"

        # output the results
        with open(out_file_name, "w") as f:
            f.write(output)

        # process the changes and commit to knowledge graph
        update_lines = triplet_updates.split('\n')
        remove_idx = update_lines.index("REMOVE:")
        add_idx = update_lines.index("ADD:")
        remove = update_lines[remove_idx + 1 : add_idx]
        add = update_lines[add_idx + 1:]

        # delete triplets from graph
        for triplet_str in remove:
            triplet = triplet_str.split(" -> ")
            if len(triplet) == 3:
                self._graph_store.delete(triplet[0], triplet[1], triplet[2])

        # add new triplets to graph
        for triplet_str in add:
            triplet = triplet_str.split(" -> ")
            if len(triplet) == 3:
                self._graph_store.upsert_triplet(triplet[0], triplet[1], triplet[2])

        print("Completed update:", state_change)

def main():

    # set API key
    openai_keys_file = os.path.join(os.getcwd(), "../keys/openai_keys.txt")
    with open(openai_keys_file, "r") as f:
        keys = f.read()
    keys = keys.strip().split('\n')
    os.environ["OPENAI_API_KEY"] = keys[0]

    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    graph_name = "knowledge_graph"
    from age_graph import AgeGraphStore
    graph_store = AgeGraphStore(
        dbname="knowledge_base",
        user="postgres",
        password="password",
        host="localhost",
        port=5432,
        graph_name=graph_name,
        node_label="entity"
    )

    llm = OpenAI(temperature=0, model="gpt-4")
    updater = KnowledgeGraphUpdater(llm=llm, graph_store=graph_store)

    # set of state changes
    state_changes = ["I put the egg in the fridge."]

    for i, state_change in enumerate(state_changes):
        updater.process_state_change(state_change, f"result{i}.txt")


if __name__ == "__main__":
    main()