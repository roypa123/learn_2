# check_rules.py - test algebra rules with many random whole numbers
import random

random.seed(1)


def distributive_left(a, b, c):
    return c * (a + b)


def distributive_right(a, b, c):
    return c * a + c * b


def square_left(a, b, c):
    return (a + b) ** 2


def square_right(a, b, c):
    return a ** 2 + 2 * a * b + b ** 2


def wrong_right(a, b, c):
    return a ** 2 + b ** 2


def check(name, left, right, trials=1000):
    for _ in range(trials):
        a = random.randint(-20, 20)
        b = random.randint(-20, 20)
        c = random.randint(-20, 20)
        if left(a, b, c) != right(a, b, c):
            print(f"{name}: FAILS at a={a}, b={b}, c={c}")
            return
    print(f"{name}: passed {trials} tests")


check("c(a + b) = ca + cb        ", distributive_left, distributive_right)
check("(a + b)^2 = a^2 + 2ab + b^2", square_left, square_right)
check("(a + b)^2 = a^2 + b^2      ", square_left, wrong_right)
