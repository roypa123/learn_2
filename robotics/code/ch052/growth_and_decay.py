# growth_and_decay.py - multiply by the same factor every step, and how logs undo it
import math

print("step  doubling  halving")
value_up = 1.0
value_down = 1.0
for step in range(0, 9):
    print(f"{step:4d} {value_up:9.0f} {value_down:9.4f}")
    value_up = value_up * 2
    value_down = value_down * 0.5

print()
print("formula 2 ** 8   =", 2 ** 8, "    log2(256) =", math.log2(256))
print("formula 10 ** 3  =", 10 ** 3, "   log10(1000) =", math.log10(1000))
print("e                =", math.e, "   ln(e) =", math.log(math.e))

rate = 0.05
doubling_steps = math.log(2) / math.log(1 + rate)
print(f"growing 5% per step doubles after {doubling_steps:.2f} steps")
