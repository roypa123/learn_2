# find_angle.py - from two sides back to the angle, with asin, acos and atan
import math

rise = 0.30
run = 4.00
length = math.hypot(rise, run)

print(f"ramp: rise {rise} m, run {run} m, sloping length {length:.4f} m")
print(f"from tan: {math.degrees(math.atan(rise / run)):.3f} degrees")
print(f"from sin: {math.degrees(math.asin(rise / length)):.3f} degrees")
print(f"from cos: {math.degrees(math.acos(run / length)):.3f} degrees")

for percent in [5, 8.33, 10, 15, 100]:
    angle = math.degrees(math.atan(percent / 100))
    print(f"a {percent:6.2f}% slope is {angle:5.2f} degrees")
