# units.py - Rover's unit conversions, each one written once and used everywhere
PI = 3.14159
WHEEL_DIAMETER_M = 0.06589         # calibrated in Chapter 16
TICKS_PER_TURN = 540


def ticks_to_metres(ticks):
    """Return the distance rolled for this many encoder ticks."""
    turns = ticks / TICKS_PER_TURN
    return turns * PI * WHEEL_DIAMETER_M


def metres_to_ticks(metres):
    """Return the whole number of ticks needed to roll this distance."""
    turns = metres / (PI * WHEEL_DIAMETER_M)
    return round(turns * TICKS_PER_TURN)


def speed_to_rpm(speed_ms):
    """Return the wheel speed in rpm for a robot speed in m/s."""
    return speed_ms / (PI * WHEEL_DIAMETER_M) * 60


print(f"2640 ticks = {ticks_to_metres(2640):.3f} m")
print(f"1 m = {metres_to_ticks(1.0)} ticks")
print(f"0.25 m/s = {speed_to_rpm(0.25):.1f} rpm")
print(f"there and back: {ticks_to_metres(metres_to_ticks(1.0)):.4f} m")
