# safe_rover.py - a Robot that refuses to do unsafe things
import math


class SafeRover:
    MAX_SPEED_MS = 0.5
    POWER_W = 3.78
    RESERVE_WH = 0.5                  # never use this last bit of energy

    def __init__(self, battery_wh):
        self.x_m = 0.0
        self.battery_wh = battery_wh
        self.refused = 0              # a counter that the object keeps for itself

    def energy_needed(self, distance_m, speed_ms):
        """Return the Wh needed for this drive."""
        return self.POWER_W * (abs(distance_m) / speed_ms) / 3600

    def drive(self, distance_m, speed_ms=0.25):
        """Drive if it is safe. Return True if the drive happened."""
        if not 0 < speed_ms <= self.MAX_SPEED_MS:
            print(f"  refused: speed {speed_ms} is not allowed")
            self.refused += 1
            return False
        needed = self.energy_needed(distance_m, speed_ms)
        if self.battery_wh - needed < self.RESERVE_WH:
            print(f"  refused: needs {needed:.3f} Wh, only {self.battery_wh:.3f} Wh left")
            self.refused += 1
            return False
        self.x_m += distance_m
        self.battery_wh -= needed
        print(f"  drove {distance_m} m: x = {self.x_m:.1f}, battery {self.battery_wh:.3f} Wh")
        return True


rover = SafeRover(battery_wh=0.6)
rover.drive(10.0)                     # needs 0.042 Wh: fine
rover.drive(1.0, speed_ms=2.0)        # too fast
rover.drive(30.0)                     # needs 0.126 Wh: would dip into the reserve
print("refused drives:", rover.refused)
