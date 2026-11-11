# parabola_parts.py - the important points of y = a x^2 + b x + c
from quadratic import solve_quadratic


def describe(a, b, c):
    vertex_x = -b / (2 * a)
    vertex_y = a * vertex_x ** 2 + b * vertex_x + c
    shape = "opens up (a lowest point)" if a > 0 else "opens down (a highest point)"
    print(f"y = {a}x^2 + {b}x + {c}")
    print(f"  {shape}")
    print(f"  vertex           : ({vertex_x:g}, {vertex_y:g})")
    print(f"  line of symmetry : x = {vertex_x:g}")
    print(f"  y-intercept      : (0, {c:g})")
    print(f"  x-intercepts     : {solve_quadratic(a, b, c)}")


describe(1, -2, -3)
describe(-0.5, 2, 1)
