# robot.py - a Robot class: one object holds its own state and knows how to move
import math


class Robot:
    """A robot on a flat floor, with a position, a heading and a battery."""

    POWER_W = 3.78                    # a class attribute: the same for every Robot

    def __init__(self, name, x_m=0.0, y_m=0.0, heading_deg=0.0, battery_wh=11.52):
        self.name = name              # instance attributes: each object has its own
        self.x_m = x_m
        self.y_m = y_m
        self.heading_deg = heading_deg
        self.battery_wh = battery_wh
        self.odometer_m = 0.0

    def turn(self, angle_deg):
        """Turn on the spot. Positive angles turn right."""
        self.heading_deg = (self.heading_deg + angle_deg) % 360

    def drive(self, distance_m, speed_ms=0.25):
        """Drive straight ahead, and use energy for the time it takes."""
        h = math.radians(self.heading_deg)
        self.x_m += distance_m * math.sin(h)
        self.y_m += distance_m * math.cos(h)
        self.odometer_m += abs(distance_m)
        self.battery_wh -= self.POWER_W * abs(distance_m) / speed_ms / 3600

    def status(self):
        """Return one line of text describing the robot."""
        return (f"{self.name}: ({self.x_m:.2f}, {self.y_m:.2f}) facing {self.heading_deg:.0f}, "
                f"driven {self.odometer_m:.2f} m, battery {self.battery_wh:.4f} Wh")


if __name__ == "__main__":
    rover = Robot("rover")
    cart = Robot("cart", x_m=5.0, heading_deg=180)

    rover.drive(2.0)
    rover.turn(90)
    rover.drive(1.5)
    cart.drive(1.0, speed_ms=0.5)

    print(rover.status())
    print(cart.status())
