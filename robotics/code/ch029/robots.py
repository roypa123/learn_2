# robots.py - one base class, several kinds of robot
import math


class Robot:
    """What every robot has in common."""

    def __init__(self, name, battery_wh):
        self.name = name
        self.battery_wh = battery_wh

    def power_w(self):
        """Return the power this robot uses while moving."""
        return 5.0

    def move(self, seconds):
        """Use energy for some time. Return a sentence about it."""
        used = self.power_w() * seconds / 3600
        self.battery_wh -= used
        return f"{self.name} moved for {seconds} s and used {used:.3f} Wh"

    def endurance_min(self):
        """Return how many minutes the battery will last."""
        return self.battery_wh / self.power_w() * 60

    def __str__(self):
        return f"{type(self).__name__} {self.name}: {self.battery_wh:.2f} Wh, {self.endurance_min():.0f} min left"


class Rover(Robot):
    """A wheeled robot: a Robot with a low power use."""

    def power_w(self):                # replaces the version in Robot
        return 3.78


class Drone(Robot):
    """A flying robot: power depends on how heavy it is."""

    def __init__(self, name, battery_wh, mass_kg):
        super().__init__(name, battery_wh)      # let Robot do its part
        self.mass_kg = mass_kg
        self.altitude_m = 0.0

    def power_w(self):
        return 150.0 * self.mass_kg ** 1.5      # a simple model, not a law of nature

    def climb(self, metres):
        self.altitude_m += metres
        return f"{self.name} is now at {self.altitude_m} m"


if __name__ == "__main__":
    fleet = [Rover("rover", 11.52), Drone("scout", 50.0, 1.0), Robot("generic", 10.0)]

    for robot in fleet:               # the same call, different behaviour
        print(robot.move(60))

    for robot in fleet:
        print(robot)

    print(fleet[1].climb(20))
    print(isinstance(fleet[0], Robot), isinstance(fleet[0], Drone))
