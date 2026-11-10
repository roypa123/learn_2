# solve_linear.py - solve a*x + b = c*x + d, the same way we do on paper
def solve_linear(a, b, c, d):
    coefficient = a - c
    number = d - b
    if coefficient == 0:
        if number == 0:
            return "every x works"
        return "no solution"
    return number / coefficient


tests = [(3, 2, 0, 14), (5, -4, 2, 8), (2, 1, 2, 5), (2, 1, 2, 1)]

for a, b, c, d in tests:
    answer = solve_linear(a, b, c, d)
    print(f"{a}x + {b} = {c}x + {d}   ->   {answer}")
