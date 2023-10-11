import os
import logging
import sys
import re
from functools import partial
from llama_index.llms.utils import LLMType
from llama_index.graph_stores.types import GraphStore
from llama_index.llms import OpenAI
from llama_index.retrievers import KnowledgeGraphRAGRetriever
from llama_index import ServiceContext
from llama_index.storage.storage_context import StorageContext

from knowledge_graph.utils import get_prompt_template, extract_keywords

TRIPLET_FILTER_PROMPT = get_prompt_template("triplet_filter_prompt.txt")
TRIPLET_UPDATE_PROMPT = get_prompt_template("triplet_update_prompt.txt")

def process_state_change(retriever: KnowledgeGraphRAGRetriever, graph_store: GraphStore, llm: LLMType,
                         state_change: str, out_file_name: str) -> None:
    output = "------------------------------------------------\n"
    output += f"STATE CHANGE: {state_change}\n"

    # retrieve relevant triplets with llama-index (but prevent llama-index printing)
    with open(os.devnull,"w") as devNull:
        orig = sys.stdout
        sys.stdout = devNull
        context_nodes = retriever.retrieve(state_change)
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
    filtered_triplet_str = llm.complete(TRIPLET_FILTER_PROMPT.format(state_change=state_change, triplet_str=triplet_str)).text
    output += "------------------------------------------------\n"
    output += "FILTERED TRIPLETS:\n\n"
    output += filtered_triplet_str + "\n"

    # query LLM to update triplets (remove existing and add new)
    triplet_updates = llm.complete(TRIPLET_UPDATE_PROMPT.format(state_change=state_change, filtered_triplet_str=filtered_triplet_str)).text
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
            graph_store.delete(triplet[0], triplet[1], triplet[2])

    # add new triplets to graph
    for triplet_str in add:
        triplet = triplet_str.split(" -> ")
        if len(triplet) == 3:
            graph_store.upsert_triplet(triplet[0], triplet[1], triplet[2])

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
    service_context = ServiceContext.from_defaults(llm=llm)
    storage_context = StorageContext.from_defaults(graph_store=graph_store)
    graph_rag_retriever = KnowledgeGraphRAGRetriever(
        storage_context=storage_context,
        service_context=service_context,
        verbose=True,
        graph_traversal_depth=1,
        max_knowledge_sequence=200,
        entity_extract_fn=partial(extract_keywords, graph_store, service_context),
        entity_extract_policy="union"
    )

    # set of state changes
    state_changes = ["I put the egg in the fridge."]

    for i, state_change in enumerate(state_changes):
        process_state_change(graph_rag_retriever, graph_store, llm, state_change, f"result{i}.txt")


if __name__ == "__main__":
    main()