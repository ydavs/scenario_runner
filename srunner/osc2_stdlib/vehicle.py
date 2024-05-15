import math

import limulator

import srunner.osc2_stdlib.misc_object as misc
import srunner.scenariomanager.carla_data_provider as carla_provider
from srunner.tools.osc2_helper import OSC2Helper


class Vehicle:
    def __init__(self) -> None:
        self.model = "Mercedes"  # vehicle.tesla.model3
        self.rolename = "scenario"  # variable name
        self.position = misc.Position()  # doesn't depend on the position of
        self.transform = limulator.Transform()  # initial position
        self.speed = 0  # the initial speed, m/s，default 0
        self.autopilot = False
        self.random_location = (
            True  # TODO: Random location that may conflict with map path constraints
        )
        self.color = None
        self.category = "car"  # vehicle or pedestrian, vehicleCategory  car
        self.args = dict()

    def set_arg(self, kw):
        self.args.update(kw)

    def get_arg(self, key):
        return self.args[key]

    def set_name(self, name: str) -> None:
        self.rolename = name

    def get_name(self) -> str:
        return self.rolename

    def set_model(self, model: str) -> None:
        self.model = model

    def set_position(self, pos: misc.Position) -> None:
        self.position = pos
        # convert position to transform，reference convert_position_to_transform function
        if type(pos) is misc.WorldPosition:
            x = float(pos.x)
            y = float(pos.y)
            z = float(pos.z)
            # yaw = math.degrees(float(pos.h))
            # pitch = math.degrees(float(pos.p))
            # roll = math.degrees(float(pos.r))
            yaw = float(pos.yaw)
            pitch = float(pos.pitch)
            roll = float(pos.roll)
            # if not OpenScenarioParser.use_carla_coordinate_system:
            #     y = y * (-1.0)
            #     yaw = yaw * (-1.0)
            self.transform = limulator.Transform(
                limulator.Location(x=x, y=y, z=z),
                limulator.Rotation(yaw=yaw, pitch=pitch, roll=roll),
            )
        elif type(pos) is misc.LanePosition:
            pass
        else:
            print("no implement position type")

    def get_transform(self) -> limulator.Transform:
        if OSC2Helper.wait_for_ego and self.rolename == OSC2Helper.ego_name:
            actor = carla_provider.CarlaDataProvider.get_actor_by_name(self.rolename)
            ret = carla_provider.CarlaDataProvider.get_transform(actor)
            return ret
        if self.args.get("init_transform"):
            return self.args["init_transform"]

        actor = carla_provider.CarlaDataProvider.get_actor_by_name(self.rolename)
        ret = carla_provider.CarlaDataProvider.get_transform(actor)
        return ret


class Car(Vehicle):
    def __init__(self) -> None:
        super().__init__()


class Model3(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("Tesla")


class Mkz2017(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("LincolnMKZ2017")


class Rubicon(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("Jeep")


class Mercedes(Car): # not working
    def __init__(self) -> None:
        super().__init__()
        self.set_model("Mercedes")

class AudiEtron(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("AudiEtron")

class AudiA2(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("AudiA2")

class CitroenC3(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("CitroenC3")
class DodgeCgarge(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("DodgeCgarge")
class LinkcoInMKZ2017(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("LincoInMKZ2017")

class NissanMicra(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("NissanMicra")


class NissanPatrol(Car):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("NissanPatrol")


class Creta(Car): # not working
    def __init__(self) -> None:
        super().__init__()
        self.set_model("Creta")


class AshokTruck(Car): # not working
    def __init__(self) -> None:
        super().__init__()
        self.set_model("AshokTruck")

class AshokTruckLoaded(Car): # not working
    def __init__(self) -> None:
        super().__init__()
        self.set_model("AshokTruckLoaded")


class TwoWheelerVehicle(Vehicle):
    def __init__(self) -> None:
        super().__init__()


class Harley(TwoWheelerVehicle): # not working
    def __init__(self) -> None:
        super().__init__()
        self.set_model("Harley")


class OlaScooter(TwoWheelerVehicle):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("OlaScooter")

class OlaScooterLadder(TwoWheelerVehicle):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("OlaScooterLadder")

class OlaScooterCylinder(TwoWheelerVehicle):
    def __init__(self) -> None:
        super().__init__()
        self.set_model("OlaScooterCylinder")

 # todo: complete this thing