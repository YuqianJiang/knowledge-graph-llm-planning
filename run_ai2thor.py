import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional
from time import sleep

from agents.kg_agent import KnowledgeGraphThorAgent
from tasks.task import Task


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="knowledge_graph_llm_planning")
    parser.add_argument('--method', type=str, choices=["knowledge_graph"],
                                              default="knowledge_graph")
    parser.add_argument('--task', type=str, default="BringCoffee")  # BringCoffee, ChillApple, CleanMug
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

    mode = "full"  # debug, full

    if mode == "debug":
        agent_update_method = "none"  # wander, text, none
        agent_plan = False
        plan_file_name = "experiments/kg/" + args.task + "/run1/plan_0.pddl"
    elif mode == "full":
        agent_update_method = "text"  # wander, text, none
        agent_plan = True  # If false, we simulate planning using a previous run
    else:
        raise ValueError("Invalid mode")

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

    t = 0
    while True:
        state_changes = task.human_step(t)
        if len(state_changes) > 0:
            print("state changed, updating agent state")
            agent.update_state(state_changes=state_changes, wander_step=10)
        if len(state_changes) > 0 or t == 0:  # replan condition
            if agent_plan:
                plan_file_name = agent.answer_planning_query(task.query)
            # wait for the plan to be ready
            while not os.path.exists(plan_file_name):
                sleep(1)
            agent.read_plan_for_execution(plan_file_name)
        succeed = agent.act()
        print("Step ", t, "succeed: ", succeed)
        t += 1

        if len(agent.plan) == 0:
            task.check_task_success()
            break
