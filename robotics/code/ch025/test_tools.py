# test_tools.py - automatic checks for our robot functions
def clamp(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return value


def heading_error(a, b):
    """Return the short way round from b to a, in degrees (-180 to 179)."""
    return (a - b + 180) % 360 - 180


assert clamp(5, 0, 1) == 1
assert clamp(-5, 0, 1) == 0
assert clamp(0.5, 0, 1) == 0.5
assert clamp(0, 0, 1) == 0              # at the edge
assert clamp(1, 0, 1) == 1              # at the other edge

assert heading_error(359, 0) == -1
assert heading_error(1, 359) == 2
assert heading_error(90, 90) == 0
assert heading_error(350, 10) == -20

print("all tests passed")
