# debouncer.py - the same Debouncer class in Python (Chapter 28), to compare with Debouncer.h and Debouncer.cpp
class Debouncer:
    def __init__(self, stable_ms=5):              # the constructor
        self.stable_ms = stable_ms
        self.stable = 1                           # HIGH: not pressed
        self.last = 1
        self.changed_at = 0
        self.presses = 0

    def update(self, level, now_ms):              # in C++ the object reads its own pin and the clock
        if level != self.last:
            self.last = level
            self.changed_at = now_ms
        if self.stable != self.last and now_ms - self.changed_at >= self.stable_ms:
            self.stable = self.last
            if self.stable == 0:
                self.presses += 1
                return True
        return False


left = Debouncer()
right = Debouncer()
# one reading per millisecond: a press with bounce on the left, a clean press on the right
left_levels = [1] * 3 + [0, 1, 0, 1, 0] + [0] * 12 + [1] * 10
right_levels = [1] * 10 + [0] * 10 + [1] * 10
for ms, (l, r) in enumerate(zip(left_levels, right_levels)):
    if left.update(l, ms):
        print(f"{ms} ms: left pressed")
    if right.update(r, ms):
        print(f"{ms} ms: right pressed")
print(f"presses: left {left.presses}, right {right.presses}")
