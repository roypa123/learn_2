# vector_monte_carlo.py - Chapter 31's test, for 100,000 runs at once
import time

import numpy as np

SETPOINT_M, MAX_SPEED_MS, DT_S, DANGER_M = 0.30, 0.25, 0.5, 0.25
RUNS, STEPS = 100_000, 20
NOISE_M = 0.03
rng = np.random.default_rng(3)        # NumPy's random number generator, with a seed


def near_misses(gain):
    """Return how many of the runs came closer than the danger limit."""
    distance = np.full(RUNS, 1.0)     # one distance for every run
    closest = distance.copy()
    for _ in range(STEPS):
        measured = distance + rng.normal(0, NOISE_M, RUNS)            # RUNS random numbers
        speed = np.clip(gain * (measured - SETPOINT_M), -MAX_SPEED_MS, MAX_SPEED_MS)
        distance -= speed * DT_S
        closest = np.minimum(closest, distance)                       # item by item
    return int(np.sum(closest < DANGER_M))


start = time.perf_counter()
for gain in (1.0, 2.0, 3.0):
    misses = near_misses(gain)
    print(f"gain {gain}: {misses:6d} near misses out of {RUNS}  ({misses / RUNS:.1%})")
print(f"total time: {time.perf_counter() - start:.3f} s")
