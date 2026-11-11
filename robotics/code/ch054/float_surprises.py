# float_surprises.py - why 0.1 + 0.2 is not exactly 0.3, and what the computer really stores
import math
from decimal import Decimal

print("0.1 + 0.2       =", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)
print("isclose         :", math.isclose(0.1 + 0.2, 0.3))
print("0.1 is really    :", Decimal(0.1))
print("2.675 is really  :", Decimal(2.675))
print("round(2.675, 2)  =", round(2.675, 2))
print("0.5 is really    :", Decimal(0.5), "(exact: a power of 2)")

total = 0.0
for _ in range(10):
    total += 0.1
print("0.1 added 10 times:", total)

print("2.0 // 0.05       =", 2.0 // 0.05, "  but 2.0 / 0.05 =", 2.0 / 0.05)
print("round(0.5), round(1.5), round(2.5):", round(0.5), round(1.5), round(2.5))
print("biggest float     :", 1.7976931348623157e308, "  times 10 =", 1.7976931348623157e308 * 10)
print("gap after 1.0     :", math.ulp(1.0), "  gap after 1e6:", math.ulp(1e6))
