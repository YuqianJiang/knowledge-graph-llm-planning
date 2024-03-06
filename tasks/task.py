from .human_actions import MoveTo, FillObjectWithLiquid, EmptyLiquidFromObject, ChangeObjectState
from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
from ai2thor.server import MetadataWrapper

class Task:
    def __init__(self, name):
        """
        A Task maintains the scene, the potential human actions, as well as the controller that steps the environment.
        """
        self.name = name
        if name == "BringCoffee":
            self.query = "Can you bring the mug with coffee to the dining table?"
            self.scene = "FloorPlan26_physics"  # "FloorPlan10"
            hum_act1 = [MoveTo('Mug', "CoffeeMachine"),
                        FillObjectWithLiquid('Mug', 'coffee')]
            self.state_changes = {0: hum_act1}

        elif name == "ChillApple":
            self.query = "Can you chill the apple?"
            self.scene = "FloorPlan10"
            self.state_changes = {0:MoveTo('Apple', "Plate")}

        elif name == "CookPotato":
            self.query = "Can you cook the patato?"
            self.scene = "FloorPlan10"
            hum_act1 = self.hide_obj_in_container("Bread", "Fridge")
            self.state_changes = {0: hum_act1}

        elif name == "CleanMug":
            self.query = "Can you put a clean mug on the dining table?"
            self.scene = "FloorPlan10"
            hum_act1 = [MoveTo('Mug', "CoffeeMachine")]
            hum_act2 = [FillObjectWithLiquid('Mug', 'coffee')]
            hum_act3 = [EmptyLiquidFromObject('Mug')]
            self.state_changes = {1: hum_act1, 2: hum_act2, 3: hum_act3}

        elif name == "Breakfast":
            self.query = "Can you put potato, bread, and egg on the dining table?"
            self.scene = "FloorPlan10"
            hum_act1 = [MoveTo('Potato', "DiningTable"), MoveTo('Egg', "DiningTable"), MoveTo('Bread', "DiningTable")]
            self.state_changes = {0: hum_act1}

        elif name == "ServeBread":
            self.query = "Can you put a bread with plate on the dining table?"
            self.scene = "FloorPlan26_physics"
            hum_act1 = [MoveTo('Bread', "Plate"), MoveTo('Plate', "DiningTable")]
            hum_act1 = self.hide_obj_in_container("Bread", "Fridge")
            self.state_changes = {0: hum_act1}
        elif name == "CleanKitchen":
            self.query = "Can you clean the kitchen?"
            # TODO: human makes something dirty along the way
        elif name == "CleanLivingRoom":
            # TODO: brainstorm more tasks in other room types
            raise NotImplementedError
        else:
            raise NotImplementedError

        # Initialize controller
        # controller = Controller(scene=f"{task.scene}", platform=CloudRendering, server_timeout=10)
        self.controller = Controller(scene=f"{self.scene}")

    def hide_obj_in_container(self, obj, container):
        assert container in ["Fridge", "Cabinet", "Microwave"]
        state_changes = [ChangeObjectState(container, "OpenObject"),
                         MoveTo(obj, container),
                         ChangeObjectState(container, "CloseObject")]
        return state_changes

    def start(self):
        """
        This function sets up the initial state of the environment.
        """
        # event = controller.step(action="InitialRandomSpawn",
        #                         randomSeed=1,
        #                         forceVisible=False,
        #                         numPlacementAttempts=5,
        #                         placeStationary=True)
        event = self.controller.step(action="Pass")

        # # List all objects in the scene
        # objects = event.metadata['objects']
        # for obj in objects:
        #     print(obj['objectType'])
        return event

    def human_step(self, time):
        """
        Returns the state changes corresponding to a specific time step.
        """
        state_changes = self.state_changes.get(time, [])
        for i, event in enumerate(state_changes):
            event.execute(self.controller)
        return state_changes
