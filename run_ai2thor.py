import argparse
import logging
import os
import sys
from pathlib import Path

from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
from ai2thor.server import MetadataWrapper

from agents.kg_agent import KnowledgeGraphThorAgent

class PersonAction:
    def execute(self, controller: Controller) -> bool:
        pass

    def to_text_update(self) -> str:
        pass

class MoveTo(PersonAction):
    def __init__(self, obj: str, to: str):
        self.obj = obj
        self.to = to
        self.next_to = None

    def to_text_update(self) -> str:
        if self.next_to:
            next_to_name = self.next_to.split("|")[0]
            return f"I moved the {self.obj} to the {self.to} next to the {next_to_name}."
        return f"I moved the {self.obj} to the {self.to}."

    def execute(self, c: Controller) -> bool:
        receptacles = [r for r in c.last_event.metadata['objects'] if r['objectType'] == self.to]
        if len(receptacles) == 0:
            return False
        receptacle = receptacles[0]

        event = controller.step('GetSpawnCoordinatesAboveReceptacle', objectId=receptacle['objectId'], anywhere=True)
        if not event.metadata['lastActionSuccess']:
            return False

        # disambiguate if there are multiple instances of the receptacle
        if len(receptacles) > 1 and len(receptacle['receptacleObjectIds']) > 0:
            self.next_to = receptacle['receptacleObjectIds'][0]

        same_type = [o for o in c.last_event.metadata['objects'] if o['objectType'] == self.obj]
        if len(same_type) == 0:
            return False
        objId = same_type[0]['objectId']

        coordinates = event.metadata['actionReturn'].copy()
        for candidate in coordinates:
            event = c.step(action='PlaceObjectAtPoint', objectId=objId,
                                    position=candidate)
            if event.metadata['lastActionSuccess']:
                return True

        return False

action_to_text = {'ToggleObjectOff': "I turned the {obj_name} off.",
                'ToggleObjectOn': "I turned the {obj_name} on.",
                'DirtyObject': "The {obj_name} is dirty.",
                'CleanObject': "I cleaned the {obj_name}.",
                'OpenObject': "I opened the {obj_name}.",
                'CloseObject': "I closed the {obj_name}.",
                'CookObject': "I cooked the {obj_name}.",
                'SliceObject': "I sliced the {obj_name}.",
                'BreakObject': "I broke the {obj_name}."}

class ChangeObjectState(PersonAction):
    def __init__(self, obj: str, action_name: str):
        self.obj = obj
        self.action_name = action_name

    def to_text_update(self) -> str:
        return action_to_text[self.action_name].format(obj_name=self.obj)

    def execute(self, c: Controller) -> bool:
        same_type = [o for o in c.last_event.metadata['objects'] if o['objectType'] == self.obj]
        if len(same_type) == 0:
            return False
        objId = same_type[0]['objectId']
        event = c.step(action=self.action_name, objectId=objId, forceAction=True)
        if event.metadata['lastActionSuccess']:
            return True
        return False


class FillObjectWithLiquid(PersonAction):
    def __init__(self, obj: str, liquid: str):
        self.obj = obj
        self.liquid = liquid

    def to_text_update(self) -> str:
        obj_name = self.obj.split("|")[0]
        return f"I filled the {obj_name} with {self.liquid}."

    def execute(self, c: Controller) -> bool:
        same_type = [o for o in c.last_event.metadata['objects'] if o['objectType'] == self.obj]
        if len(same_type) == 0:
            return False
        objId = same_type[0]['objectId']
        event = c.step(action='FillObjectWithLiquid', objectId=objId, fillLiquid=self.liquid, forceAction=True)
        if event.metadata['lastActionSuccess']:
            return True
        return False


class EmptyLiquidFromObject(PersonAction):
    def __init__(self, obj: str):
        self.obj = obj

    def to_text_update(self) -> str:
        return f"I finished the liquid in the {self.obj}."

    def execute(self, c: Controller) -> bool:
        same_type = [o for o in c.last_event.metadata['objects'] if o['objectType'] == self.obj]
        if len(same_type) == 0:
            return False
        objId = same_type[0]['objectId']
        event = c.step(action='EmptyLiquidFromObject', objectId=objId, forceAction=True)
        if not event.metadata['lastActionSuccess']:
            return False
        event = c.step(action='DirtyObject', objectId=objId, forceAction=True)
        if not event.metadata['lastActionSuccess']:
            return False
        return True


state_changes = [ChangeObjectState("Fridge", "OpenObject"),
                 MoveTo("Egg", "Fridge"),
                 ChangeObjectState("Fridge", "CloseObject")]

state_changes = [FillObjectWithLiquid('Mug', 'coffee'),
                 EmptyLiquidFromObject('Mug'),
                 MoveTo('Mug', "CounterTop")]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="knowledge_graph_llm_planning")
    parser.add_argument('--method', type=str, choices=["knowledge_graph"],
                                              default="knowledge_graph")
    parser.add_argument('--scene', type=str, default="FloorPlan10")
    parser.add_argument('--run', type=int, default=0)
    args = parser.parse_args()

    pgpass_file = os.path.expanduser("~/.pgpass")
    with open(pgpass_file, "r") as f:
        pgpass = f.read()
    pgpass = pgpass.strip().split('\n')[1].split(':')
    graph_name = "knowledge_graph"
    log_dir = Path(__file__).parent / f"experiments/kg/{args.scene}/run{args.run}/"
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

    agent = KnowledgeGraphThorAgent(
        host=pgpass[0],
        dbname=pgpass[2],
        user=pgpass[3],
        password=pgpass[4],
        port=5432,
        log_dir=log_dir.as_posix()
    )

    controller = Controller(scene=f"{args.scene}", platform=CloudRendering, server_timeout=10)
    # controller = Controller(scene=f"{args.scene}")

    event = controller.step(action="InitialRandomSpawn",
                            randomSeed=1,
                            forceVisible=False,
                            numPlacementAttempts=5,
                            placeStationary=True)
    metadata = event.metadata
    agent.load_simulation_state(metadata)

    for i, state_change in enumerate(state_changes):
        state_change.execute(controller)
        agent.input_state_change(state_change.to_text_update())

