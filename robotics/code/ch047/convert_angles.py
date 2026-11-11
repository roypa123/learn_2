# convert_angles.py - degrees to radians and back, by hand and with the math module
import math

PI = 3.141592653589793


def deg_to_rad(degrees):
    return degrees * PI / 180


def rad_to_deg(radians):
    return radians * 180 / PI


print("degrees   radians (ours)   radians (math)")
for d in [0, 30, 45, 57.2958, 90, 180, 270, 360]:
    print(f"{d:7g} {deg_to_rad(d):14.4f} {math.radians(d):16.4f}")

print("1 radian is", f"{rad_to_deg(1):.4f}", "degrees")
print("sin(90) with degrees by mistake:", f"{math.sin(90):.4f}")
print("sin(90 degrees) done properly  :", f"{math.sin(math.radians(90)):.4f}")
