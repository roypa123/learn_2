# unit_circle.py - cos and sin for any angle: the point on a circle of radius 1
import math

print(" angle      cos      sin    quadrant")
for deg in [0, 45, 90, 135, 180, 225, 270, 315, 360, 405, -45]:
    t = math.radians(deg)
    c = math.cos(t)
    s = math.sin(t)
    if abs(c) < 1e-12 or abs(s) < 1e-12:
        where = "on an axis"
    elif c > 0 and s > 0:
        where = "I"
    elif c < 0 < s:
        where = "II"
    elif c < 0 and s < 0:
        where = "III"
    else:
        where = "IV"
    print(f"{deg:6d} {c:8.3f} {s:8.3f}    {where}")
