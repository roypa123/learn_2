# monte_carlo_wall.py - drive at the wall 500 times with noise: how often is it close?
import random

random.seed(3)
SETPOINT_M = 0.30
MAX_SPEED_MS = 0.25
DT_S = 0.5
DANGER_M = 0.25                       # closer than this counts as a near miss


def one_run(gain, noise_m):
    """Simulate one approach. Return the closest distance reached."""
    distance_m = 1.0
    closest_m = distance_m
    for _ in range(20):
        measured_m = distance_m + random.gauss(0, noise_m)   # the sensor is noisy
        speed_ms = max(-MAX_SPEED_MS, min(MAX_SPEED_MS, gain * (measured_m - SETPOINT_M)))
        distance_m -= speed_ms * DT_S
        closest_m = min(closest_m, distance_m)
    return closest_m


print("gain  worst run   near misses out of 500")
for gain in (1.0, 2.0, 3.0):
    results = [one_run(gain, noise_m=0.03) for _ in range(500)]
    misses = len([c for c in results if c < DANGER_M])
    print(f"{gain:4.1f}  {min(results):.3f} m     {misses}")
