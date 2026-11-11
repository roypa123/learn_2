# ir_lookup.py - an infrared distance sensor described by a table, read both ways
TABLE = [(10, 2.30), (15, 1.65), (20, 1.30), (30, 0.92),
         (40, 0.74), (50, 0.60), (60, 0.50), (80, 0.40)]     # (cm, volts)


def volts_at(distance):
    for (d1, v1), (d2, v2) in zip(TABLE, TABLE[1:]):
        if d1 <= distance <= d2:
            return v1 + (v2 - v1) * (distance - d1) / (d2 - d1)
    return None


def distance_from_volts(volts):
    for (d1, v1), (d2, v2) in zip(TABLE, TABLE[1:]):
        if v2 <= volts <= v1:
            return d1 + (d2 - d1) * (volts - v1) / (v2 - v1)
    return None


print("distance 25 cm gives", f"{volts_at(25):.3f} V")
print("  volts   distance (cm)")
for volts in [2.30, 1.80, 1.00, 0.55, 0.30, 2.50]:
    d = distance_from_volts(volts)
    text = "outside the table" if d is None else f"{d:.1f}"
    print(f"{volts:7.2f}   {text}")
