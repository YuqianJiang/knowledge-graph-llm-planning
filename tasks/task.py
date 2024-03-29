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
            self.state_changes = [MoveTo('Apple', "Plate")]

        elif name == "CookEgg":
            state_changes = [ChangeObjectState("Fridge", "OpenObject"),
                             MoveTo("Egg", "Fridge"),
                             ChangeObjectState("Fridge", "CloseObject")]
            raise NotImplementedError

        elif name == "CleanMug":
            self.query = "Can you put a clean mug on the dining table?"
            self.scene = "FloorPlan10"
            hum_act1 = [MoveTo('Mug', "CoffeeMachine")]
            hum_act2 = [FillObjectWithLiquid('Mug', 'coffee')]
            hum_act3 = [EmptyLiquidFromObject('Mug')]
            self.state_changes = {1: hum_act1, 2: hum_act2, 3: hum_act3}
        else:
            raise NotImplementedError

        # Initialize controller
        # controller = Controller(scene=f"{task.scene}", platform=CloudRendering, server_timeout=10)
        self.controller = Controller(scene=f"{self.scene}")

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
        return event

    def human_step(self, time):
        """
        Returns the state changes corresponding to a specific time step.
        """
        state_changes = self.state_changes.get(time, [])
        for i, event in enumerate(state_changes):
            event.execute(self.controller)
        return state_changes
