# stopping.py - stopping distance = reaction distance + braking distance, and the fastest safe speed
import math

REACTION_S = 0.3          # time to notice and start braking
BRAKE = 1.5               # braking deceleration in m/s^2
FREE_SPACE_M = 2.0        # how far ahead the sensor guarantees free space


def stopping_distance(v):
    reaction_m = v * REACTION_S
    braking_m = v ** 2 / (2 * BRAKE)
    return reaction_m, braking_m


print(" speed   reaction   braking    total")
for v in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
    r, b = stopping_distance(v)
    print(f"{v:4.1f} m/s  {r:6.3f} m  {b:6.3f} m  {r + b:6.3f} m")

# fastest safe speed: v^2/(2 BRAKE) + REACTION_S v - FREE_SPACE_M = 0, a quadratic (Chapter 45)
qa = 1 / (2 * BRAKE)
qb = REACTION_S
qc = -FREE_SPACE_M
v_safe = (-qb + math.sqrt(qb ** 2 - 4 * qa * qc)) / (2 * qa)
print(f"fastest safe speed for {FREE_SPACE_M} m of free space: {v_safe:.4f} m/s")
print(f"check: stopping distance at that speed = {sum(stopping_distance(v_safe)):.4f} m")
