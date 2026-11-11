# odometry_sum.py - Rover's position is a sum of small steps
import math

steps = [(0.10, 0), (0.10, 0), (0.10, 15), (0.10, 30), (0.10, 45),
         (0.10, 60), (0.10, 75), (0.10, 90), (0.10, 90), (0.10, 90)]   # (distance m, heading deg)

x = sum(d * math.cos(math.radians(h)) for d, h in steps)
y = sum(d * math.sin(math.radians(h)) for d, h in steps)
path = sum(d for d, h in steps)

print(f"path length (sum of d_i)          : {path:.3f} m")
print(f"x = sum of d_i cos(theta_i)       : {x:.3f} m")
print(f"y = sum of d_i sin(theta_i)       : {y:.3f} m")
print(f"straight-line distance from start : {math.hypot(x, y):.3f} m")
