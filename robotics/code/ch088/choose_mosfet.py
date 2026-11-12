# choose_mosfet.py - which MOSFET for which robot load? Heat = I^2 x R_on, temperature rise = heat x theta
ROOM = 25.0
parts = [
    # name, R_on at 4.5 V gate (ohm), max current (A), theta to air (C/W), case
    ("2N7000 (tiny)", 1.8, 0.2, 300, "TO-92"),
    ("AO3400 (small SMD)", 0.033, 5.0, 125, "SOT-23"),
    ("IRLZ44N (logic level)", 0.025, 47.0, 62, "TO-220, no heat sink"),
    ("modern 30 V power FET", 0.003, 100.0, 40, "on a copper board"),
]
loads = [("LED strip", 0.5), ("Rover motor stall", 1.5), ("12 V fan", 2.0), ("big wheel motor", 10.0), ("drone motor", 30.0)]

print(f"{'load':18s}" + "".join(f"{p[0]:>24s}" for p in parts))
for lname, amps in loads:
    cells = []
    for name, r, imax, theta, case in parts:
        if amps > imax:
            cells.append("too small")
            continue
        heat = amps ** 2 * r
        temp = ROOM + heat * theta
        cells.append(f"{heat:6.3f} W {temp:5.0f} C" + (" HOT" if temp > 100 else ""))
    print(f"{lname:18s}" + "".join(f"{c:>24s}" for c in cells))
print()
print("compare a BJT switching the 0.5 A LED strip: 0.2 V x 0.5 A = 0.1 W plus 25 mA of base current from the pin")
