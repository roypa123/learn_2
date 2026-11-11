# arm_reach.py - can a two-link arm reach this point?
import math

UPPER_M = 0.40      # first link
FORE_M = 0.25       # second link

nearest = abs(UPPER_M - FORE_M)
furthest = UPPER_M + FORE_M
print(f"reachable ring: from {nearest:.2f} m to {furthest:.2f} m from the shoulder")
print(f"area the tip can reach: {math.pi * (furthest ** 2 - nearest ** 2):.3f} m^2")

for target in [(0.30, 0.40), (0.60, 0.20), (0.10, 0.05), (0.0, 0.65), (0.5, 0.5)]:
    d = math.dist((0, 0), target)
    ok = nearest <= d <= furthest
    print(f"target {target}: distance {d:.3f} m -> {'reachable' if ok else 'NOT reachable'}")
