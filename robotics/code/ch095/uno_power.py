# uno_power.py - how hot does the Uno's 5 V regulator get when the board is powered from the barrel jack or VIN?
DIODE = 0.8                  # V lost in the reverse-protection diode (Chapter 86)
DROPOUT = 1.1                # V the regulator needs between its input and its 5 V output (Chapter 90)
THETA = 100.0                # the small regulator on the board: about 100 C per watt (Chapter 76)
SAFE_W = 1.0                 # keep the regulator's heat under about 1 W

print(f"lowest input that still gives 5 V: 5 + {DROPOUT} + {DIODE} = {5 + DROPOUT + DIODE:.1f} V")
print()
print(f"{'input':>6s} {'current':>8s} {'heat':>7s} {'hotter by':>10s}")
for v_in in [7.0, 9.0, 12.0]:
    for ma in [50, 150, 300, 500]:              # 50 mA is the bare board; the rest is your LEDs, sensors...
        heat = (v_in - DIODE - 5.0) * ma / 1000   # the regulator burns the extra voltage times the current
        note = "" if heat <= SAFE_W else "  TOO HOT"
        print(f"{v_in:5.0f} V {ma:5d} mA {heat:6.2f} W {heat * THETA:7.0f} C{note}")
    max_ma = SAFE_W / (v_in - DIODE - 5.0) * 1000
    print(f"        -> at {v_in:.0f} V, keep the 5 V current under about {max_ma:.0f} mA")
