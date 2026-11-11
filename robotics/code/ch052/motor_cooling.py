# motor_cooling.py - how long must a hot motor rest before it may run again?
import math

ROOM_C = 25.0
TAU_S = 300.0            # time constant of this motor, from a test
START_C = 90.0
SAFE_C = 50.0


def temperature(t_s):
    return ROOM_C + (START_C - ROOM_C) * math.exp(-t_s / TAU_S)


wait_s = TAU_S * math.log((START_C - ROOM_C) / (SAFE_C - ROOM_C))
print(f"wait {wait_s:.1f} s ({wait_s / 60:.1f} min) to cool from {START_C} to {SAFE_C} C")

print("  time (s)   temperature (C)   share of the gap still left")
for t in [0, 150, 300, 600, 900, 1500]:
    left = (temperature(t) - ROOM_C) / (START_C - ROOM_C)
    print(f"{t:10d} {temperature(t):17.1f} {left:20.1%}")
