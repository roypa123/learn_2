# my_sqrt.py - find a square root by improving a guess (Heron's method)
import math


def my_sqrt(number, steps=6):
    if number < 0:
        raise ValueError("no real square root of a negative number")
    if number == 0:
        return 0.0
    guess = number / 2
    for step in range(1, steps + 1):
        guess = (guess + number / guess) / 2
        print(f"step {step}: guess = {guess:.10f}")
    return guess


answer = my_sqrt(13)
print("mine      :", answer)
print("math.sqrt :", math.sqrt(13))
print("difference:", abs(answer - math.sqrt(13)))
