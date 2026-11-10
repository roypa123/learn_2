# fake_sensor.py - any object with a read() method can be used as a sensor
class FakeSensor:
    """Returns numbers from a list: perfect for testing without hardware."""

    def __init__(self, readings):
        self.readings = readings
        self.index = 0

    def read(self):
        value = self.readings[self.index]
        self.index = (self.index + 1) % len(self.readings)     # go round and round
        return value


class BrokenSensor:
    """Always fails, so that we can test what the robot does then."""

    def read(self):
        raise OSError("sensor not responding")


def wall_ahead(sensor, limit_m=0.3):
    """Return True if a wall is close. A failed sensor counts as a wall."""
    try:
        return sensor.read() < limit_m
    except OSError:
        return True                   # fail-safe (Chapter 17)


assert wall_ahead(FakeSensor([0.2])) is True
assert wall_ahead(FakeSensor([0.9])) is False
assert wall_ahead(FakeSensor([0.3])) is False       # exactly at the limit
assert wall_ahead(BrokenSensor()) is True

sensor = FakeSensor([0.9, 0.5, 0.25])
print([wall_ahead(sensor) for _ in range(4)])
print("all tests passed")
