# scan_to_xy.py - turn laser readings (distance and angle) into x and y in front of the robot
import math

readings = [(-60, 2.31), (-30, 1.73), (0, 1.50), (30, 1.73), (60, 3.00)]   # (degrees, metres)

print("angle   range     x (forward)   y (left)")
for deg, r in readings:
    t = math.radians(deg)
    x = r * math.cos(t)
    y = r * math.sin(t)
    print(f"{deg:5d} {r:7.2f} {x:13.3f} {y:10.3f}")
