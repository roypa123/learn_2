# reverse_protection.py - protect Rover from a battery put in backwards: what does each method cost?
V_BATT = 7.2
methods = [
    # name, voltage lost when the battery is the right way round (at 0.53 A and at 3.1 A)
    ("nothing (no protection)", 0.0, 0.0),
    ("silicon diode in series (1N5400)", 0.80, 0.95),
    ("Schottky diode in series (SB540)", 0.38, 0.50),
    ("P-channel MOSFET (Chapter 88), 0.02 ohm", 0.53 * 0.02, 3.1 * 0.02),
]
print(f"{'method':42s} {'lost at 0.53 A':>15s} {'heat':>8s} {'lost at 3.1 A':>14s} {'heat':>8s}")
for name, v1, v2 in methods:
    print(f"{name:42s} {v1:12.3f} V {v1 * 0.53 * 1000:5.0f} mW {v2:11.3f} V {v2 * 3.1 * 1000:5.0f} mW")
print()
print("battery reversed:")
print("  no protection: the motor driver and the Arduino get -7.2 V and are destroyed in a moment")
print("  any of the three: the diode or MOSFET blocks, nothing flows, nothing is harmed")
print()
print(f"share of Rover's energy lost while driving: silicon {0.80 / V_BATT:.1%}, Schottky {0.38 / V_BATT:.1%}, MOSFET {0.53 * 0.02 / V_BATT:.2%}")
