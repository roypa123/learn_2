# rotate_points.py - turn a shape about the origin using sin and cos
import math

SHAPE = [(0, 0), (2, 0), (2, 1), (0, 1)]


def rotate(points, degrees):
    t = math.radians(degrees)
    c = math.cos(t)
    s = math.sin(t)
    return [(x * c - y * s, x * s + y * c) for x, y in points]


for angle in [90, 30, 180]:
    turned = rotate(SHAPE, angle)
    text = ", ".join(f"({x:.3f}, {y:.3f})" for x, y in turned)
    print(f"{angle:4d} degrees: {text}")

corner = rotate([(2, 1)], 30)[0]
print("distance from origin before:", round(math.hypot(2, 1), 4), " after:", round(math.hypot(*corner), 4))
