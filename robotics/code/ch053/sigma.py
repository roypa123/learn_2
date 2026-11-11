# sigma.py - the sigma sign is a for loop
import math

n = 100
total = 0
for i in range(1, n + 1):          # sum of i, for i = 1 to 100
    total = total + i
print("sum of i     :", total, "  formula n(n+1)/2       =", n * (n + 1) // 2)

squares = sum(i * i for i in range(1, n + 1))
print("sum of i*i   :", squares, "formula n(n+1)(2n+1)/6 =", n * (n + 1) * (2 * n + 1) // 6)

errors = [0.012, -0.008, 0.015, -0.003, 0.009, -0.011]     # metres
N = len(errors)
mean = sum(errors) / N
mean_abs = sum(abs(e) for e in errors) / N
rms = math.sqrt(sum(e * e for e in errors) / N)
print(f"mean error {mean * 1000:.2f} mm, mean size {mean_abs * 1000:.2f} mm, RMS {rms * 1000:.2f} mm")
