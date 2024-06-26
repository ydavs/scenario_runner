import random
import sys

from srunner.osc2_dm.physical_types import Physical
from srunner.osc2_stdlib.misc_object import AVCarSide, ScenarioEvent
from srunner.osc2_stdlib.vehicle import Vehicle


class Modifier:
    def __init__(self, actor_name: str, name: str) -> None:
        self.actor_name = actor_name
        self.name = name
        self.args = {}

    def set_args(self, kw_args) -> None:
        self.args = kw_args

    def get_name(self) -> str:
        return self.name

    def get_actor_name(self) -> str:
        return self.actor_name

    def __str__(self) -> str:
        s = f"{self.name}("
        for key, value in self.args.items():
            s += str(key) + ":" + str(value) + ","
        return s + ")"


class SpeedModifier(Modifier):
    # speed([speed: ]<speed>, [faster_than: <car> | slower_than: <car>][, at: <event>], [turn: <string>])
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)
        self.args = {}

    def set_speed(self, speed) -> None:
        self.args["speed"] = speed

    def get_speed(self):
        speed = self.args["speed"]
        if isinstance(speed, Physical):
            return Physical(speed.gen_single_value(), speed.unit)
        else:
            print("[Error] 'speed' parameter of SpeedModifier must be 'Physical' type")
            sys.exit(1)

    def get_turn(self):
        if "turn" not in self.args.keys():
            return None

        turn = self.args["turn"]
        if turn == "left" or turn == "right":
            return turn
        else:
            print(
                "[Error] 'side' parameter of PositionModifier must be 'Physical' type"
            )
            sys.exit(1)

    def set_relative_car(self, car: Vehicle, side: AVCarSide) -> None:
        self.args[side] = car

    def set_trigger_point(self, trigger_point: ScenarioEvent) -> None:
        self.args["at"] = trigger_point


class PositionModifier(Modifier):
    # position([distance: ]<distance> | time: <time>, [ahead_of: <car> | behind: <car>], [at: <event>])
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_distance(self):
        dist = self.args["distance"]
        if isinstance(dist, Physical):
            return dist
        else:
            print(
                "[Error] 'distance' parameter of PositionModifier must be 'Physical' type"
            )
            sys.exit(1)

    def get_refer_car(self):
        if self.args.get("ahead_of"):
            return self.args.get("ahead_of"), "ahead_of"
        elif self.args.get("behind"):
            return self.args.get("behind"), "behind"
        else:
            print("PositionModifier key error")

    def get_trigger_point(self) -> str:
        return self.args.get("at", "all")
class TurnModifier(Modifier):
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_side(self):
        side = self.args["side"]
        if side=="left" or side=="right" or side=="straight":
            return side
        else:
            print(
                "[Error] 'side' parameter of PositionModifier must be 'Physical' type"
            )
            sys.exit(1)

    def get_trigger_point(self) -> str:
        return self.args.get("at", "all")
class WrongSideModifier(Modifier):
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_status(self):
        status = self.args["activate"]
        if status==True or status==False:
            return status
        else:
            print(
                "[Error] 'status' parameter of PositionModifier must be Boolean type"
            )
            sys.exit(1)

    def get_trigger_point(self) -> str:
        return self.args.get("at", "all")
class RoadActionModifier(Modifier):
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_status(self):
        if"wrong_side" in self.args.keys():
            status = self.args["wrong_side"]
            if status==True or status==False:
                return status
            else:
                print(
                    "[Error] 'status' parameter of PositionModifier must be Boolean type"
                )
                sys.exit(1)
        else:
            return None
    
    def get_turn_side(self):
        if"turn" in self.args.keys():
            side = self.args["turn"]
            if side=="left" or side=="right" or side=="straight":
                return side
            else:
                print(
                    "[Error] 'side' parameter of PositionModifier must be 'Physical' type"
                )
                sys.exit(1)
        else:
            return None
    
    def get_speed(self):
        speed = self.args["speed"]
        if isinstance(speed, Physical):
            return Physical(speed.gen_single_value(), speed.unit)
        else:
            print("[Error] 'speed' parameter of SpeedModifier must be 'Physical' type")
            sys.exit(1)

    def get_trigger_point(self) -> str:
        return self.args.get("at", "all")

class OrientationModifier(Modifier):
    # position([distance: ]<distance> | time: <time>, [ahead_of: <car> | behind: <car>], [at: <event>])
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_yaw(self):
        yaw = self.args["yaw"]
        if isinstance(yaw, Physical):
            return yaw
        else:
            print(
                "[Error] 'yaw' parameter of PositionModifier must be 'Physical' type"
            )
            sys.exit(1)
    def get_pitch(self):
        pitch = self.args["pitch"]
        if isinstance(pitch, Physical):
            return pitch
        else:
            print(
                "[Error] 'pitch' parameter of PositionModifier must be 'Physical' type"
            )
            sys.exit(1)
    def get_roll(self):
        roll = self.args["roll"]
        if isinstance(roll, Physical):
            return roll
        else:
            print(
                "[Error] 'roll' parameter of PositionModifier must be 'Physical' type"
            )
            sys.exit(1)

    def get_refer_car(self):
        if self.args.get("ahead_of"):
            return self.args.get("ahead_of"), "ahead_of"
        elif self.args.get("behind"):
            return self.args.get("behind"), "behind"
        elif self.args.get("relative_to"):
            return self.args.get("relative_to"), "relative_to"
        else:
            print("PositionModifier key error")

    def get_trigger_point(self) -> str:
        return self.args.get("at", "all")

class LaneModifier(Modifier):
    # lane([[lane: ]<lane>][right_of | left_of | same_as: <car>] | [side_of: <car>, side: <av-side>][at: <event>])
    # <av-side> is right or left.
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_refer_car(self):
        if self.args.get("right_of"):
            return self.args.get("right_of"), "right_of"
        elif self.args.get("left_of"):
            return self.args.get("left_of"), "left_of"
        elif self.args.get("same_as"):
            return self.args.get("same_as"), "same_as"
        elif self.args.get("side_of"):
            return self.args.get("side_of"), self.args.get("side")
        else:
            return None

    def get_lane_id(self):
        return self.args.get("lane")

    def get_trigger_point(self) -> str:
        return self.args.get("at", "all")


class ChangeSpeedModifier(Modifier):
    # change_speed([speed: ]<speed>)
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_speed(self):
        desired_speed = self.args["desired_speed"]
        if isinstance(desired_speed, Physical):
            return Physical(desired_speed.gen_single_value(), desired_speed.unit)
        else:
            print(
                "[Error] 'desired_speed' parameter of ChangeSpeedModifier must be 'Physical' type"
            )
            sys.exit(1)


class ChangeLaneModifier(Modifier):
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_lane_changes(self):
        if len(self.args.values()) == 1:
            return 1
        else:
            if (
                self.args["lane_changes"][0] != "["
                and self.args["lane_changes"][-1] != "]"
            ):
                return int(float(self.args["lane_changes"]))
            else:
                values = self.args["lane_changes"][1:-1].split("..")
                start = int(float(values[0]))
                end = int(float(values[1]))
                value = random.randint(start, end)
                return value

    def get_side(self):
        for value in self.args.values():
            if value == "right":
                return "right"
            elif value == "left":
                return "left"
        else:
            print("ChangeLaneModifier has no such position define")


class AccelerationModifier(Modifier):
    def __init__(self, actor_name: str, name: str) -> None:
        super().__init__(actor_name, name)

    def get_accelerate(self):
        return self.args["acceleration"]
