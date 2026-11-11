# plane_basics.py - quadrants, midpoints and grid distance for points on a plane
def quadrant(x, y):
    if x == 0 or y == 0:
        return "on an axis"
    if x > 0 and y > 0:
        return "I"
    if x < 0 and y > 0:
        return "II"
    if x < 0 and y < 0:
        return "III"
    return "IV"


def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def grid_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


for point in [(3, 2), (-4, 1), (-2, -3), (5, -1), (0, 4)]:
    print(f"{point} is in quadrant: {quadrant(point[0], point[1])}")

a = (1, 1)
b = (5, 4)
print("midpoint of a and b :", midpoint(a, b))
print("grid distance a to b:", grid_distance(a, b))
