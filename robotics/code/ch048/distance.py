# distance.py - straight-line distance with Pythagoras, in 2D and 3D
import math


def distance_2d(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return math.sqrt(dx * dx + dy * dy)


def distance_3d(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dz = b[2] - a[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


print("(1, 1) to (5, 4)     :", distance_2d((1, 1), (5, 4)))
print("(0, 0) to (2, 3)     :", round(distance_2d((0, 0), (2, 3)), 4))
print("math.dist agrees     :", round(math.dist((0, 0), (2, 3)), 4))
print("box corner (3, 4, 12):", distance_3d((0, 0, 0), (3, 4, 12)))
for sides in [(3, 4, 5), (5, 12, 13), (4, 5, 6)]:
    a, b, c = sides
    print(f"{sides}: right angle? {a * a + b * b == c * c}")
