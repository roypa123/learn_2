# flower_bed.py - a mower drives once round a round flower bed: how far does each wheel go?
import math

BED_RADIUS_M = 1.5          # the flower bed
GAP_M = 0.30                # from the bed edge to the robot's centre
TRACK_M = 0.40              # distance between the mower's wheels
WHEEL_RADIUS_M = 0.10

path_radius = BED_RADIUS_M + GAP_M
inner = path_radius - TRACK_M / 2
outer = path_radius + TRACK_M / 2

for name, r in [("centre", path_radius), ("inner wheel", inner), ("outer wheel", outer)]:
    length = 2 * math.pi * r
    turns = length / (2 * math.pi * WHEEL_RADIUS_M)
    print(f"{name:12s}: circle radius {r:.2f} m, distance {length:.3f} m, wheel turns {turns:.2f}")

print(f"outer wheel must go {outer / inner:.3f} times as fast as the inner wheel")
print(f"area of the bed: {math.pi * BED_RADIUS_M ** 2:.2f} m^2")
