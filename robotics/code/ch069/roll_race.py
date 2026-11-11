# roll_race.py - which reaches the bottom of a slope first: a ring, a disc, a ball or a sliding block?
import math

G = 9.81
ANGLE_DEG = 10
LENGTH_M = 2.0

# I = k m r^2 for each shape, so rolling uses up a share k of the energy in turning
shapes = [("sliding block (no friction)", None), ("solid ball", 2 / 5), ("solid disc or cylinder", 1 / 2), ("thin ring or hoop", 1.0)]
for name, k in shapes:
    if k is None:
        a = G * math.sin(math.radians(ANGLE_DEG))                  # nothing to spin up
    else:
        a = G * math.sin(math.radians(ANGLE_DEG)) / (1 + k)        # from energy: m g h = 1/2 m v^2 (1 + k)
    t = math.sqrt(2 * LENGTH_M / a)
    v = a * t
    print(f"{name:28s} a = {a:.3f} m/s^2, reaches the bottom in {t:.3f} s at {v:.3f} m/s")
