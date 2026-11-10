# bits_table.py - how many values can n bits hold, and how fine is each step?
FULL_SCALE_V = 5.0

print("bits     levels  smallest step (V)")
for bits in [1, 2, 3, 8, 10, 12, 16]:
    levels = 2 ** bits
    step = FULL_SCALE_V / levels
    print(f"{bits:4d} {levels:10d} {step:18.6f}")
