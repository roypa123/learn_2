# path_2d.py - path length and displacement for a robot driving through waypoints
import math

waypoints = [(0.0, 0.0), (4.0, 0.0), (4.0, 3.0), (1.0, 3.0), (1.0, 5.0)]

path_m = 0.0
for i in range(1, len(waypoints)):
    x0, y0 = waypoints[i - 1]
    x1, y1 = waypoints[i]
    leg_m = math.hypot(x1 - x0, y1 - y0)
    path_m = path_m + leg_m
    print(f"leg {i}: ({x0}, {y0}) -> ({x1}, {y1})   {leg_m:.2f} m")

dx = waypoints[-1][0] - waypoints[0][0]
dy = waypoints[-1][1] - waypoints[0][1]
straight_m = math.hypot(dx, dy)
heading_deg = math.degrees(math.atan2(dy, dx))

print(f"path length:   {path_m:.2f} m")
print(f"displacement:  ({dx:+.1f}, {dy:+.1f}) m, size {straight_m:.2f} m, direction {heading_deg:.1f} deg")
print(f"straightness:  {straight_m / path_m:.0%}")
