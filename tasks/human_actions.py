from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
from ai2thor.server import MetadataWrapper
from typing import Optional


action_to_text = {'ToggleObjectOff': "I turned the {obj_name} off.",
                'ToggleObjectOn': "I turned the {obj_name} on.",
                'DirtyObject': "The {obj_name} is dirty.",
                'CleanObject': "I cleaned the {obj_name}.",
                'OpenObject': "I opened the {obj_name}.",
                'CloseObject': "I closed the {obj_name}.",
                'CookObject': "I cooked the {obj_name}.",
                'SliceObject': "I sliced the {obj_name}.",
                'BreakObject': "I broke the {obj_name}."}


class PersonAction:
    def execute(self, controller: Controller) -> bool:
        pass

    def to_text_update(self) -> str:
        pass


class MoveTo(PersonAction):
    def __init__(self, obj: str, to: str, next_to: Optional[str] = None):
        self.obj = obj
        self.to = to
        self.next_to = next_to

    def to_text_update(self) -> str:
        if self.next_to:
            next_to_name = self.next_to.split("|")[0]
            return f"I moved the {self.obj} to the {self.to} next to the {next_to_name}."
        return f"I moved the {self.obj} to the {self.to}."

    def execute(self, c: Controller) -> bool:
        receptacles = [r for r in c.last_event.metadata['objects'] if r['objectType'] == self.to]
        if len(receptacles) == 0:
            return False

        if self.next_to:
            receptacle = None
            for recep in receptacles:
                if len([obj for obj in recep['receptacleObjectIds'] if self.next_to in obj]) > 0:
                    receptacle = recep
                    break
            if receptacle is None:
                return False
        # disambiguate if there are multiple instances of the receptacle
        elif len(receptacles) == 1:
            receptacle = receptacles[0]
        else:
            return False

        event = c.step('GetSpawnCoordinatesAboveReceptacle', objectId=receptacle['objectId'], anywhere=True)
        if not event.metadata['lastActionSuccess']:
            return False

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


# THis not only empties the liquid but also makes the object dirty
class EmptyLiquidFromObject(PersonAction):
    def __init__(self, obj: str):
        self.obj = obj

    def to_text_update(self) -> str:
        return f"I finished the drink in the {self.obj}."

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

