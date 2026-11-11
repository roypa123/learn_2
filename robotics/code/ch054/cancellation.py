# cancellation.py - subtracting two nearly equal numbers loses digits
import math

a, b, c = 1.0, -1e8, 1.0
root = math.sqrt(b * b - 4 * a * c)
small_naive = (-b - root) / (2 * a)
big = (-b + root) / (2 * a)
small_safe = c / (a * big)
print("small root, plain formula :", small_naive)
print("small root, using c/(a*big):", small_safe)
print("true small root is about   : 1.00000000000000000e-08")

for x in [1e-2, 1e-4, 1e-6, 1e-8]:
    naive = 1 - math.cos(x)
    safe = 2 * math.sin(x / 2) ** 2
    print(f"x = {x:7.0e}: 1 - cos x = {naive:.6e}   2 sin^2(x/2) = {safe:.6e}")
