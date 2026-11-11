# slope_and_line.py - the slope between two points, and the line y = mx + c through them
def slope(p, q):
    run = q[0] - p[0]
    rise = q[1] - p[1]
    if run == 0:
        return None
    return rise / run


def line_through(p, q):
    m = slope(p, q)
    if m is None:
        return None
    c = p[1] - m * p[0]
    return m, c


pairs = [((1, 1), (5, 4)), ((0, 3), (4, 1)), ((-2, 2), (3, 2)), ((2, -1), (2, 5))]

for p, q in pairs:
    line = line_through(p, q)
    if line is None:
        print(f"{p} to {q}: vertical line, x = {p[0]}")
    else:
        m, c = line
        print(f"{p} to {q}: slope {m:+.3f}, y = {m:.3f}x + {c:.3f}")
