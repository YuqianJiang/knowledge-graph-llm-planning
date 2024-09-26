from .human_actions import MoveTo, FillObjectWithLiquid, EmptyLiquidFromObject, ChangeObjectState
from ai2thor.controller import Controller
from ai2thor.platform import CloudRendering
from ai2thor.server import MetadataWrapper
import ipdb

def calculate_centroid(vertices):
    n = len(vertices)
    if n == 0:
        return None

    sum_x = sum(vertex['x'] for vertex in vertices)
    sum_y = sum(vertex['y'] for vertex in vertices)
    sum_z = sum(vertex['z'] for vertex in vertices)

    centroid_x = sum_x / n
    centroid_y = sum_y / n
    centroid_z = sum_z / n

    return {
        'x': centroid_x,
        'y': centroid_y,
        'z': centroid_z
    }

def print_objects(scene):
    for obj in scene['objects']:
        print(obj['assetId'])


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
            self.target_object = "Mug"
            self.target_state = 'isFilledWithLiquid'
            self.state_changes = {0: hum_act1}

        elif name == "FreezeApple":
            self.query = "Can you freeze the apple?"
            self.scene = "FloorPlan10"
            self.target_object = "Apple"
            self.target_state = 'temperature'
            # self.state_changes = {0: MoveTo('Apple', "Plate"), 1: MoveTo('Plate', "Microwave")}
            self.state_changes = {0: [MoveTo('Apple', "Microwave")]}

        elif name == "CookPotato":
            self.query = "Can you heat the patato?"
            self.scene = "FloorPlan10"
            self.target_object = "Potato"
            self.target_state = 'temperature'
            hum_act1 = [MoveTo("Potato", "Fridge")]
            self.state_changes = {0: hum_act1}

        elif name == "CleanUpKitchen":
            # TODO: this is not working: some objects are not cleaned
            self.query = "Can you clean all objects in the kitchen?"
            self.scene = "FloorPlan10"
            self.target_object = "Plate"
            self.target_state = 'isDirty'
            hum_act1 = [ChangeObjectState('Plate', "DirtyObject"),
                        ChangeObjectState('Pot', "DirtyObject"),
                        ChangeObjectState('Mug', "DirtyObject")]
            # hum_act2 = [MoveTo('Plate', "Fridge"), MoveTo('Mug', "Fridge")]
            self.state_changes = {0: hum_act1}

        elif name == "CleanMug":
            # TODO: something wrong with this: unable to get the diningtable
            self.query = "Can you put a clean mug on the dining table?"
            self.scene = "FloorPlan26_physics"
            self.target_object = "Mug"
            self.target_state = 'isDirty'
            hum_act1 = [MoveTo('Mug', "CoffeeMachine")]
            hum_act2 = [FillObjectWithLiquid('Mug', 'coffee')]
            hum_act3 = [EmptyLiquidFromObject('Mug')]
            self.state_changes = {0: hum_act1, 1: hum_act2, 2: hum_act3}

        elif name == "ServeBreakfast":
            self.query = "Can you put potato, bread, and egg on the dining table sequentially?"
            self.scene = "FloorPlan26_physics"
            self.target_object = "Potato"
            self.target_state = 'parentReceptacles'
            hum_act1 = [MoveTo('Potato', "Fridge"), MoveTo('Egg', "Fridge"), MoveTo('Bread', "Fridge")]
            self.state_changes = {0: hum_act1}

        elif name == "ServeBread":
            self.query = "Can you put a bread with plate on the dining table?"
            self.scene = "FloorPlan26_physics" # TODO: maybe this bread is too large
            self.target_object = "Bread"
            self.target_state = 'parentReceptacles'
            # hum_act1 = [MoveTo('Bread', "Plate"), MoveTo('Plate', "DiningTable")]  # This will solve the task
            hum_act1 = [MoveTo("Bread", "Fridge")]
            self.state_changes = {0: hum_act1}

        ##### Bedroom tasks #####
        elif name == "TossPhone":
            self.query = "Can you throw the phone into the garbage can?"
            self.scene = "FloorPlan326"
            self.target_object = "CellPhone"
            self.target_state = 'parentReceptacles'
            self.state_changes = {0: [MoveTo('CellPhone', "Bed")]}
        elif name == "PlacePillow":
            self.query = "Can you place all the pillows on the bed?"
            self.scene = "FloorPlan323" # This is the only environment with a sofa
            self.target_object = "Pillow"
            self.target_state = 'parentReceptacles'
            hum_act1 = [MoveTo('Pillow', "Sofa")]
            self.state_changes = {0: hum_act1}
        else:
            raise NotImplementedError

        use_cloud_render = False

        import prior
        import os
        OBJAVERSE_HOUSES_DIR = "/home/jiahenghu/project/spoc-robot-training/objaverse_houses/houses_2023_07_28"
        OBJAVERSE_ASSETS_DIR = "/home/jiahenghu/project/spoc-robot-training/objaverse_assets/2023_07_28/assets"
        def split_to_procthor_houses():
            # TODO: this would be for more diverse (but non-interactable objects)
            # max_houses_per_split = {"train": 64, "val": 0, "test": 0}
            # train_houses = prior.load_dataset(
            #     dataset="spoc-data",
            #     entity="spoc-robot",
            #     revision="local-objaverse-procthor-houses",
            #     path_to_splits=None,
            #     split_to_path={
            #         k: os.path.join(OBJAVERSE_HOUSES_DIR, f"{k}.jsonl.gz")
            #         for k in ["train", "val", "test"]
            #     },
            #     max_houses_per_split=max_houses_per_split,
            # )
            train_houses = prior.load_dataset(
                dataset="procthor-100k", entity="roseh-ai2", revision="tiny"
            )
            return train_houses

        houses = split_to_procthor_houses()


        test_objectthor = True
        if test_objectthor:
            try:
                from ai2thor.hooks.procedural_asset_hook import (
                    ProceduralAssetHookRunner,
                    get_all_asset_ids_recursively,
                    create_assets_if_not_exist,
                )
            except ImportError:
                raise ImportError(
                    "Cannot import `ProceduralAssetHookRunner`. Please install the appropriate version of ai2thor:\n"
                    f"```\npip install --extra-index-url https://ai2thor-pypi.allenai.org"
                    f" ai2thor==0+5e43486351ac6339c399c199e601c9dd18daecc3\n```"
                )
            class ProceduralAssetHookRunnerResetOnNewHouse(ProceduralAssetHookRunner):
                def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    self.last_asset_id_set = set()

                def Initialize(self, action, controller):
                    if self.asset_limit > 0:
                        return controller.step(
                            action="DeleteLRUFromProceduralCache", assetLimit=self.asset_limit
                        )

                def CreateHouse(self, action, controller):
                    house = action["house"]
                    asset_ids = get_all_asset_ids_recursively(house["objects"], [])
                    asset_ids_set = set(asset_ids)
                    if not asset_ids_set.issubset(self.last_asset_id_set):
                        controller.step(action="DeleteLRUFromProceduralCache", assetLimit=0)
                        self.last_asset_id_set = set(asset_ids)

                    return create_assets_if_not_exist(
                        controller=controller,
                        asset_ids=asset_ids,
                        asset_directory=self.asset_directory,
                        asset_symlink=self.asset_symlink,
                        stop_if_fail=self.stop_if_fail,
                    )

            # _ACTION_HOOK_RUNNER = ProceduralAssetHookRunnerResetOnNewHouse(
            #     asset_directory=OBJAVERSE_ASSETS_DIR, asset_symlink=True, verbose=True, asset_limit=200
            # )
            _ACTION_HOOK_RUNNER = None

            self.controller = Controller(scene=f"{self.scene}", action_hook_runner=_ACTION_HOOK_RUNNER) # TODO: load in a scene from objectThor
            self.controller.reset(houses["train"][0])


            scene = houses["train"][0]
            number_of_houses = len(scene['rooms'])
            room_location = {}
            for room in scene['rooms']:
                vertices = room['floorPolygon']
                centroids = calculate_centroid(vertices)
                print(centroids)
                room_location[room['id']] = centroids

            teleport_event = self.controller.step(
                action="TeleportFull",
                **scene["metadata"]["agent"],  # forceAction=True
            )

            if not teleport_event.metadata["lastActionSuccess"]:
                print("FAILED TO TELEPORT AGENT AFTER INITIALIZATION", scene)
                return teleport_event

            event = self.controller.step(action="Pass")

            print(room_location)
            # TODO: @yuqian: here, we can decide what to store into the database (check room_location)
            #   In this particular scene, a task that requires distances can be throw away the eggs into the trash can
            import ipdb; ipdb.set_trace()
        else:
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

    def check_task_success(self):
        info = self.controller.step(action="Pass")
        same_type = [o for o in info.metadata['objects'] if o['objectType'] == self.target_object]
        print(f"The final {self.target_state} of {self.target_object} is:")
        print(same_type[0][self.target_state])