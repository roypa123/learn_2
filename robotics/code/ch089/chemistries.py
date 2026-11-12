# chemistries.py - which battery chemistry for which robot? Energy per kilogram, life, power and safety
chem = [
    # name, nominal V per cell, Wh per kg, full cycles, max continuous discharge (C), rechargeable, notes
    ("alkaline (AA)", 1.5, 110, 1, 0.5, False, "cheap, one use, weak at high current"),
    ("NiMH (AA)", 1.2, 80, 500, 2, True, "safe and forgiving (Rover)"),
    ("lead-acid", 2.0, 35, 300, 1, True, "heavy, cheap, old warehouse robots"),
    ("LiFePO4", 3.2, 140, 3000, 3, True, "very safe, long life: AGVs, farm robots"),
    ("Li-ion (18650)", 3.6, 240, 800, 3, True, "high energy: laptops, e-bikes, humanoids"),
    ("LiPo (pouch)", 3.7, 180, 300, 50, True, "huge current: drones"),
]
print(f"{'chemistry':16s} {'V/cell':>7s} {'Wh/kg':>6s} {'cycles':>7s} {'max C':>6s}  notes")
for name, v, whkg, cycles, c, rech, note in chem:
    print(f"{name:16s} {v:7.1f} {whkg:6d} {cycles:7d} {c:6.1f}  {note}")

print()
print("mass of a 14.4 Wh battery (Rover's) in each chemistry, cells only:")
for name, v, whkg, *_ in chem:
    print(f"  {name:16s} {14.4 / whkg * 1000:5.0f} g")
