# ball_fit.py - a goalkeeper robot fits a parabola through three sightings of a ball
from solve_3x3 import solve_3x3

sightings = [(6.0, 0.60), (5.0, 1.05), (4.0, 1.30)]     # (distance from goal line, height) in m

rows = [[x * x, x, 1, y] for x, y in sightings]          # a x^2 + b x + c = y
a, b, c = solve_3x3(rows)
print(f"path: y = {a:.4f} x^2 + {b:.4f} x + {c:.4f}")

for x, y in sightings:
    print(f"  check x = {x}: curve gives {a * x * x + b * x + c:.4f}, seen {y}")

height_at_goal = c                                       # x = 0 on the goal line
print(f"height when it crosses the goal line: {height_at_goal:.3f} m")
