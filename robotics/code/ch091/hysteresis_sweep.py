# hysteresis_sweep.py - how wide must a Schmitt trigger's gap be? Count how many lines a robot "sees"
import math
import random

DT = 1e-5
NOISE = 0.25                                  # volts of motor noise (standard deviation)


def count_lines(gap, seed):
    """Robot drives over ONE black line: the sensor rises 0->5 V, stays, then falls 5->0 V. Count rising edges."""
    random.seed(seed)
    up, down = 2.5 + gap / 2, 2.5 - gap / 2
    state, rising = 0, 0
    t = 0.0
    while t < 0.04:
        clean = 5.0 / (1 + math.exp(-(t - 0.01) / 0.0015)) - 5.0 / (1 + math.exp(-(t - 0.03) / 0.0015))
        v = clean + random.gauss(0, NOISE)
        if state == 0 and v > up:
            state, rising = 1, rising + 1
        elif state == 1 and v < down:
            state = 0
        t += DT
    return rising


print(f"one black line, noise {NOISE} V; lines counted in 5 runs:")
for gap in [0.0, 0.2, 0.5, 1.0, 1.5, 2.0]:
    counts = [count_lines(gap, s) for s in range(5)]
    print(f"  gap {gap:3.1f} V (up {2.5 + gap / 2:.2f}, down {2.5 - gap / 2:.2f}): {counts}")
