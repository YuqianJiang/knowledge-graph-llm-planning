import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional



from agents.kg_agent import KnowledgeGraphThorAgent
from tasks.task import Task


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="knowledge_graph_llm_planning")
    parser.add_argument('--method', type=str, choices=["knowledge_graph"],
                                              default="knowledge_graph")
    parser.add_argument('--task', type=str, default="BringCoffee")
    parser.add_argument('--run', type=int, default=0)
    args = parser.parse_args()

    pgpass_file = os.path.expanduser("~/.pgpass")
    with open(pgpass_file, "r") as f:
        pgpass = f.read()
    pgpass = pgpass.strip().split('\n')[1].split(':')
    graph_name = "knowledge_graph"
    log_dir = Path(f"./experiments/kg/{args.task}/run{args.run}/")
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    task = Task(name=args.task)

    agent = KnowledgeGraphThorAgent(
        controller=task.controller,
        host=pgpass[0],
        dbname=pgpass[2],
        user=pgpass[3],
        password=pgpass[4],
        port=5432,
        log_dir=log_dir.as_posix(),
    )

    event = task.start()
    agent.load_simulation_state(event.metadata)

    for t in range(10):
        task.human_step()

    agent_update_method = "none"
    if agent_update_method == "wander":
        for i in range(100):
            agent.wander()
    elif agent_update_method == "text":
        state_changes = task.state_changes  # TODO: if this is a dictionary, how should we handle it?
        for i, state_change in enumerate(state_changes):
            agent.input_state_change(state_change.to_text_update())
    elif agent_update_method == "none":
        pass
    else:
        raise NotImplementedError

    agent_plan = False
    if agent_plan:
        query = task.query
        agent.answer_planning_query(query)


