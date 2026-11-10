# composed_rover.py - a robot built out of parts: objects inside an object
class Battery:
    def __init__(self, capacity_wh):
        self.capacity_wh = capacity_wh
        self.level_wh = capacity_wh

    def use(self, wh):
        self.level_wh = max(self.level_wh - wh, 0.0)

    @property
    def percent(self):                # used without brackets: battery.percent
        return self.level_wh / self.capacity_wh * 100


class Motor:
    MAX_SPEED_MS = 0.5

    def __init__(self):
        self._speed_ms = 0.0          # the underscore means "private: use the property"

    @property
    def speed_ms(self):
        return self._speed_ms

    @speed_ms.setter
    def speed_ms(self, value):        # runs whenever someone assigns to speed_ms
        self._speed_ms = max(-self.MAX_SPEED_MS, min(self.MAX_SPEED_MS, value))


class Rover:
    POWER_W = 3.78

    def __init__(self):
        self.battery = Battery(11.52)     # a Rover HAS a battery
        self.left = Motor()               # and HAS two motors
        self.right = Motor()

    def drive(self, left_ms, right_ms, seconds):
        self.left.speed_ms = left_ms      # the setter clamps these
        self.right.speed_ms = right_ms
        self.battery.use(self.POWER_W * seconds / 3600)
        return (self.left.speed_ms + self.right.speed_ms) / 2     # forward speed


rover = Rover()
print("forward speed:", rover.drive(0.2, 0.3, 600))
print("forward speed:", rover.drive(9.0, -9.0, 600))
print(f"left motor: {rover.left.speed_ms}   right motor: {rover.right.speed_ms}")
print(f"battery: {rover.battery.percent:.1f} %")
