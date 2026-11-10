# sensor_filter.py - a filter object remembers its own recent readings
class MovingAverage:
    """Average of the last few readings. Each object keeps its own history."""

    def __init__(self, window):
        self.window = window
        self.history = []             # a new, separate list for every object

    def update(self, value):
        """Add one reading and return the new average."""
        self.history.append(value)
        if len(self.history) > self.window:
            self.history.pop(0)       # forget the oldest reading
        return sum(self.history) / len(self.history)


front = MovingAverage(3)
left = MovingAverage(5)

front_readings = [10, 12, 9, 11, 30, 10]
left_readings = [50, 52, 51, 49, 50, 48]

for f_raw, l_raw in zip(front_readings, left_readings):
    print(f"front {f_raw:3d} -> {front.update(f_raw):5.1f}    left {l_raw:3d} -> {left.update(l_raw):5.1f}")

print("front remembers", front.history)
print("left remembers", left.history)
