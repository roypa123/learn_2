# rearrange_check.py - every rearranged formula must give back the value we started with
d = 240.0      # metres
v = 0.6        # metres per second
n = 3          # stops
s = 20.0       # seconds per stop

T = d / v + n * s

print(f"T from the formula: {T:.3f} s")
print(f"d = (T - n s) v    : {(T - n * s) * v:.3f}")
print(f"v = d / (T - n s)  : {d / (T - n * s):.3f}")
print(f"n = (T - d/v) / s  : {(T - d / v) / s:.3f}")
print(f"s = (T - d/v) / n  : {(T - d / v) / n:.3f}")
