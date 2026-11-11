# solve_2x2.py - two equations, two unknowns: a1 x + b1 y = c1 and a2 x + b2 y = c2
def solve_2x2(a1, b1, c1, a2, b2, c2):
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return x, y


if __name__ == "__main__":
    systems = [
        (1, 1, 10, 1, -1, 2),
        (2, 3, 12, 1, -1, 1),
        (1, 1, 2, 2, 2, 8),
        (1, 1, 2, 2, 2, 4),
    ]
    for a1, b1, c1, a2, b2, c2 in systems:
        answer = solve_2x2(a1, b1, c1, a2, b2, c2)
        text = "no single answer" if answer is None else f"x = {answer[0]:g}, y = {answer[1]:g}"
        print(f"{a1}x + {b1}y = {c1}  and  {a2}x + {b2}y = {c2}   ->  {text}")
