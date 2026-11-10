# rover_math.py - tools used by many Rover programs: import this file
import math

WHEEL_DIAMETER_M = 0.06589
TICKS_PER_TURN = 540


def clamp(value, low, high):
    """Return value, but never below low or above high."""
    return max(low, min(value, high))


def ticks_to_metres(ticks):
    """Return the distance rolled for this many encoder ticks."""
    return ticks / TICKS_PER_TURN * math.pi * WHEEL_DIAMETER_M


def heading_error(a_deg, b_deg):
    """Return the short way round from b to a, in degrees (-180 to 179)."""
    return (a_deg - b_deg + 180) % 360 - 180


def move(x_m, y_m, heading_deg, distance_m):
    """Return the new (x, y) after driving on a compass heading (0 = north)."""
    h = math.radians(heading_deg)
    return x_m + distance_m * math.sin(h), y_m + distance_m * math.cos(h)


if __name__ == "__main__":             # only when this file is run directly
    assert clamp(5, 0, 1) == 1
    assert heading_error(359, 0) == -1
    assert math.isclose(move(0, 0, 90, 1)[0], 1.0)
    print("rover_math: all tests passed")
