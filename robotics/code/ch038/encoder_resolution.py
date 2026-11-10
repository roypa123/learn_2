# encoder_resolution.py - how much do more bits help the tip of an arm?
import math

ARM_LENGTH_M = 0.8

print("bits     counts  step (deg)  tip step (mm)")
for bits in [10, 12, 14, 17, 20]:
    counts = 2 ** bits
    step_deg = 360 / counts
    tip_step_mm = 2 * math.pi * ARM_LENGTH_M / counts * 1000
    print(f"{bits:4d} {counts:10d} {step_deg:11.5f} {tip_step_mm:14.4f}")
