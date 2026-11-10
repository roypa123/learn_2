# fractions_by_hand.py - simplify, add and multiply fractions the way you do on paper


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def simplify(top, bottom):
    divisor = gcd(top, bottom)
    return top // divisor, bottom // divisor


def add(a, b, c, d):
    return simplify(a * d + c * b, b * d)


def multiply(a, b, c, d):
    return simplify(a * c, b * d)


def divide(a, b, c, d):
    return multiply(a, b, d, c)


print("gcd of 12 and 60:", gcd(12, 60))
print("12/60 simplified:", simplify(12, 60))
print("1/2 + 1/3       :", add(1, 2, 1, 3))
print("1/5 x 1/3       :", multiply(1, 5, 1, 3))
print("3/4 / 1/8       :", divide(3, 4, 1, 8))
