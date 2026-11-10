# gain_sweep.py - try many gains automatically, and find the fastest one that behaves
SETPOINT_M = 0.30
MAX_SPEED_MS = 0.25
DEADBAND_M = 0.01
DT_S = 0.5
MAX_STEPS = 60

best_gain = 0.0
best_steps = MAX_STEPS

print("gain  steps  lowest distance")
for k in range(1, 9):                     # k = 1, 2, ... 8
    gain = k * 0.5                        # count with an int, then calculate the float
    distance_m = 1.0
    lowest_m = distance_m
    steps = MAX_STEPS

    for step in range(MAX_STEPS):         # one run of the wall simulation (Chapter 19)
        error_m = distance_m - SETPOINT_M
        if abs(error_m) < DEADBAND_M:
            steps = step                  # settled: remember how long it took
            break
        speed_ms = gain * error_m
        if speed_ms > MAX_SPEED_MS:
            speed_ms = MAX_SPEED_MS
        elif speed_ms < -MAX_SPEED_MS:
            speed_ms = -MAX_SPEED_MS
        distance_m -= speed_ms * DT_S
        if distance_m < lowest_m:
            lowest_m = distance_m

    print(f"{gain:4.1f} {steps:6d} {lowest_m:12.3f}")
    no_overshoot = lowest_m >= SETPOINT_M - DEADBAND_M
    if no_overshoot and steps < best_steps:
        best_steps = steps
        best_gain = gain

print("best gain without overshoot:", best_gain, "in", best_steps, "steps")
