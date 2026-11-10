# sensor_calibration.py - compare a sensor with a ruler, and fit a straight line
import random

import matplotlib.pyplot as plt

random.seed(5)
true_m = [0.1 * i for i in range(1, 16)]
# this sensor reads 4% too high, 2 cm too high, with some noise
measured_m = [1.04 * t + 0.02 + random.gauss(0, 0.008) for t in true_m]

n = len(true_m)
mean_t = sum(true_m) / n
mean_m = sum(measured_m) / n
top = sum((t - mean_t) * (m - mean_m) for t, m in zip(true_m, measured_m))
bottom = sum((t - mean_t) ** 2 for t in true_m)
slope = top / bottom                  # the best straight line: least squares
offset = mean_m - slope * mean_t

corrected_m = [(m - offset) / slope for m in measured_m]
worst_before = max(abs(m - t) for m, t in zip(measured_m, true_m))
worst_after = max(abs(c - t) for c, t in zip(corrected_m, true_m))

print(f"measured = {slope:.4f} x true + {offset:.4f}")
print(f"worst error before: {worst_before * 100:.1f} cm")
print(f"worst error after:  {worst_after * 100:.1f} cm")

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(true_m, measured_m, color="tab:blue", label="measured")
ax.plot(true_m, [slope * t + offset for t in true_m], color="tab:red", label="best-fit line")
ax.plot(true_m, true_m, color="black", linestyle="--", label="perfect sensor")
ax.set_xlabel("true distance (m)")
ax.set_ylabel("sensor reading (m)")
ax.grid(True)
ax.legend()
fig.savefig("calibration.png", dpi=150)
