from .human_actions import MoveTo, FillObjectWithLiquid, EmptyLiquidFromObject, ChangeObjectState
from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
from ai2thor.server import MetadataWrapper
import ipdb

class Task:
    def __init__(self, name):
        """
        A Task maintains the scene, the potential human actions, as well as the controller that steps the environment.
        """
        # TODO: test a few behavior tasks, based on the human actions currently available
        self.name = name
        if name == "BringCoffee":
            self.query = "Can you bring the mug with coffee to the dining table?"
            self.scene = "FloorPlan26_physics"  # "FloorPlan10"
            hum_act1 = [MoveTo('Mug', "CoffeeMachine"),
                        FillObjectWithLiquid('Mug', 'coffee')]
            self.state_changes = {0: hum_act1}

        elif name == "FreezeApple":
            self.query = "Can you freeze the apple?"
            self.scene = "FloorPlan10"
            # self.state_changes = {0: MoveTo('Apple', "Plate"), 1: MoveTo('Plate', "Microwave")}
            self.state_changes = {0: [MoveTo('Apple', "Microwave")]}

        elif name == "CookPotato":
            self.query = "Can you heat the patato?"
            self.scene = "FloorPlan10"
            hum_act1 = self.hide_obj_in_container("Potato", "Fridge")
            self.state_changes = {0: hum_act1}

        elif name == "CleanUpKitchen":
            self.query = "Can you clean all objects in the kitchen?"
            self.scene = "FloorPlan10"
            hum_act1 = [ChangeObjectState('Plate', "DirtyObject"),
                        ChangeObjectState('Pot', "DirtyObject"),
                        ChangeObjectState('Mug', "DirtyObject")]
            # hum_act2 = [MoveTo('Plate', "Fridge"), MoveTo('Mug', "Fridge")]
            self.state_changes = {0: hum_act1}

        elif name == "CleanMug":
            self.query = "Can you put a clean mug on the dining table?"
            self.scene = "FloorPlan10"
            hum_act1 = [MoveTo('Mug', "CoffeeMachine")]
            hum_act2 = [FillObjectWithLiquid('Mug', 'coffee')]
            hum_act3 = [EmptyLiquidFromObject('Mug')]
            self.state_changes = {1: hum_act1, 2: hum_act2, 3: hum_act3}

        elif name == "ServeBreakfast":
            self.query = "Can you put potato, bread, and egg on the dining table sequentially?"
            self.scene = "FloorPlan10"
            hum_act1 = [MoveTo('Potato', "Fridge"), MoveTo('Egg', "Fridge"), MoveTo('Bread', "Fridge")]
            self.state_changes = {0: hum_act1}

        elif name == "ServeBread":
            self.query = "Can you put a bread with plate on the dining table?"
            self.scene = "FloorPlan26_physics"
            # hum_act1 = [MoveTo('Bread', "Plate"), MoveTo('Plate', "DiningTable")]  # This will solve the task
            hum_act1 = self.hide_obj_in_container("Bread", "Fridge")
            self.state_changes = {0: hum_act1}

        ##### Bedroom tasks #####
        elif name == "TossPhone":
            self.query = "Can you break the phone and throw it to the garbage can?"
            self.scene = "FloorPlan326"
            self.state_changes = {0: [MoveTo('Phone', "Bed")]}
        elif name == "PlacePillow":
            self.query = "Can you place the pillow on the bed?"
            self.scene = "FloorPlan326"
            hum_act1 = [MoveTo('Pillow', "Sofa")]
            self.state_changes = {0: hum_act1}
        else:
            raise NotImplementedError

        use_cloud_render = False
        # Initialize controller
        if use_cloud_render:
            self.controller = Controller(scene=f"{self.scene}", platform=CloudRendering, server_timeout=10)
        else:
            self.controller = Controller(scene=f"{self.scene}")

    def hide_obj_in_container(self, obj, container):
        # TODO: seems like this is not necessary -> move to is enough
        assert container in ["Fridge", "Cabinet", "Microwave"]
        state_changes = [ChangeObjectState(container, "OpenObject"),
                         MoveTo(obj, container),
                         ChangeObjectState(container, "CloseObject")]
        return state_changes

    def start(self):
        """
        This function sets up the initial state of the environment.
        """
        randomize_intial_state = False
        if randomize_intial_state:
            event = self.controller.step(action="InitialRandomSpawn",
                                         randomSeed=1,
                                         forceVisible=False,
                                         numPlacementAttempts=5,
                                         placeStationary=True)
        else:
            event = self.controller.step(action="Pass")

        # TODO: set to true to list all objects in the scene
        print_object_types = False
        if print_object_types:
            objects = event.metadata['objects']
            for obj in objects:
                print(obj['objectType'])
        return event

    def human_step(self, time):
        """
        Returns the state changes corresponding to a specific time step.
        """
        state_changes = self.state_changes.get(time, [])
        for i, event in enumerate(state_changes):
            suceess = event.execute(self.controller)
            if not suceess:
                print(f"Action {i} failed: {event}")
                ipdb.set_trace()
        return state_changes
