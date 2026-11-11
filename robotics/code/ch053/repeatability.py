# repeatability.py - how close together does an arm put its tip, time after time?
import math

# tip positions measured in mm, relative to the taught point, after 10 visits
visits = [(0.02, -0.01), (0.03, 0.02), (-0.01, 0.01), (0.04, 0.00), (0.01, -0.02),
          (0.02, 0.03), (0.00, 0.01), (0.03, -0.01), (0.05, 0.02), (0.01, 0.00)]

N = len(visits)
mean_x = sum(x for x, y in visits) / N
mean_y = sum(y for x, y in visits) / N
distances = [math.hypot(x - mean_x, y - mean_y) for x, y in visits]
mean_d = sum(distances) / N
spread = math.sqrt(sum((d - mean_d) ** 2 for d in distances) / (N - 1))
repeatability = mean_d + 3 * spread

print(f"centre of the visits : ({mean_x:.3f}, {mean_y:.3f}) mm")
print(f"offset from target   : {math.hypot(mean_x, mean_y):.3f} mm  (accuracy)")
print(f"mean distance to centre: {mean_d:.4f} mm, spread {spread:.4f} mm")
print(f"repeatability (mean + 3 x spread): {repeatability:.3f} mm")
