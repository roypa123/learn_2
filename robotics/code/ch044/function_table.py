# function_table.py - one input, one output: a table of values for four functions
import math


def double_plus_one(x):
    return 2 * x + 1


def square(x):
    return x * x


def reciprocal(x):
    if x == 0:
        return None
    return 1 / x


def root(x):
    if x < 0:
        return None
    return math.sqrt(x)


print("   x   2x+1   x*x    1/x   sqrt(x)")
for x in [-2, -1, 0, 0.5, 1, 2, 4]:
    values = [double_plus_one(x), square(x), reciprocal(x), root(x)]
    cells = ["  ---" if v is None else f"{v:6.2f}" for v in values]
    print(f"{x:4}", " ".join(cells))
