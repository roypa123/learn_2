# quadratic.py - solve a x^2 + b x + c = 0 with the quadratic formula
import math


def solve_quadratic(a, b, c):
    if a == 0:
        raise ValueError("not a quadratic: a is 0")
    disc = b * b - 4 * a * c
    if disc < 0:
        return ()
    if disc == 0:
        return (-b / (2 * a),)
    root = math.sqrt(disc)
    x1 = (-b - root) / (2 * a)
    x2 = (-b + root) / (2 * a)
    return tuple(sorted((x1, x2)))


if __name__ == "__main__":
    tests = [(1, -5, 6), (1, -4, 4), (1, 2, 5), (2, 3, -2), (1, -2, -3)]
    for a, b, c in tests:
        roots = solve_quadratic(a, b, c)
        shown = ", ".join(f"{r:g}" for r in roots) if roots else "no real solution"
        print(f"{a}x^2 + {b}x + {c} = 0   disc = {b * b - 4 * a * c:3d}   x = {shown}")
