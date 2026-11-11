# clock_drift.py - adding up a small time step for an hour, in different ways
import numpy as np

DT = 0.001                 # a 1000 Hz control loop
STEPS = 3_600_000          # one hour

t32 = np.float32(0.0)
dt32 = np.float32(DT)
t64 = 0.0
ticks = 0
checkpoints = {60_000, 600_000, 3_600_000}

print("  true time (s)   float32 sum   float64 sum    integer ticks")
for step in range(1, STEPS + 1):
    t32 = t32 + dt32
    t64 = t64 + DT
    ticks += 1
    if step in checkpoints:
        true = step * DT
        print(f"{true:15.0f} {float(t32):13.3f} {t64:13.6f} {ticks / 1000:16.3f}")
