# solve_triangle.py - any triangle: law of cosines and law of sines
import math


def angles_from_sides(a, b, c):
    A = math.acos((b * b + c * c - a * a) / (2 * b * c))
    B = math.acos((a * a + c * c - b * b) / (2 * a * c))
    C = math.pi - A - B
    return math.degrees(A), math.degrees(B), math.degrees(C)


def side_from_two_sides(a, b, C_deg):
    C = math.radians(C_deg)
    return math.sqrt(a * a + b * b - 2 * a * b * math.cos(C))


def side_from_sines(known_side, known_angle_deg, other_angle_deg):
    return known_side * math.sin(math.radians(other_angle_deg)) / math.sin(math.radians(known_angle_deg))


print("sides 3, 4, 5      -> angles", [round(x, 2) for x in angles_from_sides(3, 4, 5)])
print("sides 5, 6, 7      -> angles", [round(x, 2) for x in angles_from_sides(5, 6, 7)])
print("a=5, b=7, C=60     -> c =", round(side_from_two_sides(5, 7, 60), 4))
print("a=3, b=4, C=90     -> c =", round(side_from_two_sides(3, 4, 90), 4))
print("a=10 opposite 40, B=75 -> b =", round(side_from_sines(10, 40, 75), 4))
