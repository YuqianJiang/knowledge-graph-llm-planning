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
    parser.add_argument('--task', type=str, default="BringCoffee") # BringCoffee, ChillApple, CleanMug
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

    agent_update_method = "none"  # wander, text, none
    agent = KnowledgeGraphThorAgent(
        controller=task.controller,
        host=pgpass[0],
        dbname=pgpass[2],
        user=pgpass[3],
        password=pgpass[4],
        port=5432,
        log_dir=log_dir.as_posix(),
        update_method=agent_update_method
    )

    event = task.start()
    agent.load_simulation_state(event.metadata)

    agent_plan = False  # If false, we simulate planning using a previous run
    for t in range(8):
        state_changes = task.human_step(t)
        agent.update_state(state_changes=state_changes, wander_step=10)
        if len(state_changes) > 0 or t == 0:  # replan condition
            if agent_plan:
                plan_file_name = agent.answer_planning_query(task.query)
            else:
                plan_file_name = "experiments/kg/FloorPlan26_physics/run3/plan_0.pddl"
            agent.read_plan_for_execution(plan_file_name)
        succeed = agent.act()
        print("Step ", t, "succeed: ", succeed)

        # TODO: terminate when the task is done

