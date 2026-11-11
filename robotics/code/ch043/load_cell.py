# load_cell.py - two-point calibration turns raw counts into kilograms
RAW_EMPTY = 8421          # reading with nothing on the scale
RAW_KNOWN = 52713         # reading with the known weight on it
KNOWN_KG = 2.000          # the known weight

m = KNOWN_KG / (RAW_KNOWN - RAW_EMPTY)
c = -m * RAW_EMPTY

print(f"slope m     = {m:.4e} kg per count")
print(f"intercept c = {c:.4f} kg")
print("   raw    mass (kg)")
for raw in [8421, 30567, 52713, 61000, 7900]:
    mass = m * raw + c
    print(f"{raw:6d} {mass:12.3f}")
