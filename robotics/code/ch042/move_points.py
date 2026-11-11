# move_points.py - slide, flip and resize a shape made of points
SHAPE = [(0, 0), (2, 0), (2, 1), (0, 1)]


def translate(points, dx, dy):
    return [(x + dx, y + dy) for x, y in points]


def flip_x_axis(points):
    return [(x, -y) for x, y in points]


def scale(points, factor):
    return [(x * factor, y * factor) for x, y in points]


print("start     :", SHAPE)
print("translated:", translate(SHAPE, 3, 2))
print("flipped   :", flip_x_axis(SHAPE))
print("scaled    :", scale(SHAPE, 2))
