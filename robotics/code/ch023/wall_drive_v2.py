# wall_drive_v2.py - Chapter 19's control loop, now built from small functions
SETPOINT_M = 0.30
GAIN = 1.0
MAX_SPEED_MS = 0.25
DEADBAND_M = 0.01
DT_S = 0.5
MAX_STEPS = 50


def clamp(value, low, high):
    """Return value, but never below low or above high."""
    if value < low:
        return low
    if value > high:
        return high
    return value


def speed_command(distance_m):
    """Work out the speed for this distance to the wall."""
    error_m = distance_m - SETPOINT_M
    return clamp(GAIN * error_m, -MAX_SPEED_MS, MAX_SPEED_MS)


def arrived(distance_m):
    """Return True when Rover is close enough to the setpoint."""
    return abs(distance_m - SETPOINT_M) < DEADBAND_M


distance_m = 1.0
steps = 0
while not arrived(distance_m) and steps < MAX_STEPS:
    speed_ms = speed_command(distance_m)
    distance_m -= speed_ms * DT_S
    steps += 1

print("stopped after", steps, "steps at", round(distance_m, 3), "m")
