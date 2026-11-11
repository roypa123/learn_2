# ema_filter.py - an exponential moving average smooths a noisy distance sensor
import math
import random

random.seed(4)
DT = 0.02                  # 50 readings per second
ALPHA = 0.1                # how much of each new reading to trust

tau = -DT / math.log(1 - ALPHA)
print(f"alpha {ALPHA}: time constant {tau:.3f} s")

smooth = 1.00
print(" time   true   reading   smoothed")
for i in range(0, 51):
    t = i * DT
    true = 1.00 if t < 0.2 else 0.60          # an object steps in at t = 0.2 s
    reading = true + random.gauss(0, 0.03)
    smooth = smooth + ALPHA * (reading - smooth)
    if i % 5 == 0:
        print(f"{t:5.2f} {true:6.2f} {reading:9.3f} {smooth:10.3f}")

print(f"after one time constant the filter should have moved {1 - math.exp(-1):.1%} of the way")
