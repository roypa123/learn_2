# find_e.py - grow by 100% in total, but in smaller and smaller pieces
import math

print("        pieces n      (1 + 1/n) ** n")
for n in [1, 2, 4, 12, 365, 10_000, 1_000_000]:
    print(f"{n:15,d}   {(1 + 1 / n) ** n:.6f}")
print(f"{'math.e':>15}   {math.e:.6f}")
