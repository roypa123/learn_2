# atan_vs_atan2.py - why atan(y / x) gets half the directions wrong
import math

points = [(1, 1, 45), (-1, 1, 135), (-1, -1, -135), (1, -1, -45), (0, 2, 90), (-3, 0, 180)]

print("   point   true direction   atan(y/x)   atan2(y, x)")
for x, y, true_deg in points:
    if x == 0:
        plain = "divide by 0"
    else:
        plain = f"{math.degrees(math.atan(y / x)):8.1f}"
    good = math.degrees(math.atan2(y, x))
    print(f"{str((x, y)):>9} {true_deg:12d}     {plain:>11} {good:12.1f}")
