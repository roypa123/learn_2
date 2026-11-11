# room_survey.py - from tape measurements to a floor plan, an area and a check
import math

from survey_data import CHECKS, DIAGONALS, SIDES


def angle_from_sides(opposite, side1, side2):
    cos_angle = (side1 ** 2 + side2 ** 2 - opposite ** 2) / (2 * side1 * side2)
    return math.acos(max(-1.0, min(1.0, cos_angle)))


def place_corners(sides, diagonals):
    corners = {"A": (0.0, 0.0), "B": (sides["AB"], 0.0)}
    direction = 0.0
    fan = [("B", "C", sides["AB"], diagonals["AC"], sides["BC"]),
           ("C", "D", diagonals["AC"], diagonals["AD"], sides["CD"]),
           ("D", "E", diagonals["AD"], sides["EA"], sides["DE"])]
    for _, new, near, far, across in fan:
        direction += angle_from_sides(across, near, far)
        corners[new] = (far * math.cos(direction), far * math.sin(direction))
    return corners


def shoelace_area(points):
    total = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def triangle_area(a, b, c):
    angle = angle_from_sides(c, a, b)
    return 0.5 * a * b * math.sin(angle)


if __name__ == "__main__":
    corners = place_corners(SIDES, DIAGONALS)
    for name, (x, y) in corners.items():
        print(f"corner {name}: ({x:6.3f}, {y:6.3f}) m")

    ring = [corners[k] for k in "ABCDE"]
    by_triangles = (triangle_area(SIDES["AB"], SIDES["BC"], DIAGONALS["AC"])
                    + triangle_area(DIAGONALS["AC"], SIDES["CD"], DIAGONALS["AD"])
                    + triangle_area(DIAGONALS["AD"], SIDES["DE"], SIDES["EA"]))
    print(f"perimeter         : {sum(SIDES.values()):.3f} m")
    print(f"area, 3 triangles : {by_triangles:.3f} m^2")
    print(f"area, shoelace    : {shoelace_area(ring):.3f} m^2")

    for pair, measured in CHECKS.items():
        computed = math.dist(corners[pair[0]], corners[pair[1]])
        print(f"check {pair}: measured {measured:.3f}, from the plan {computed:.3f}, "
              f"difference {1000 * (computed - measured):+.1f} mm")
