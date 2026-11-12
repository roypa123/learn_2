# linear_reg.py - a linear regulator turns the extra voltage into heat: Rover's 5 V rail from a falling battery
V_OUT = 5.0
I_LOAD = 0.19                     # Rover's 5 V rail (Chapter 77)
THETA = 50.0                      # TO-220 regulator with no heat sink, C per W (Chapter 76)
REGULATORS = {"7805 (old, needs 2 V extra)": 2.0, "LDO (needs 0.3 V extra)": 0.3}

print(f"5 V at {I_LOAD * 1000:.0f} mA from Rover's battery as it empties (6 x NiMH: 8.4 V full, 6.0 V empty)")
print(f"{'battery':>8s} {'heat':>8s} {'temp rise':>10s} {'efficiency':>11s}   " + "   ".join(REGULATORS))
for v_in in [8.4, 7.6, 7.2, 6.8, 6.4, 6.0]:
    heat = (v_in - V_OUT) * I_LOAD                 # same current in and out; the voltage difference becomes heat
    eff = V_OUT / v_in                             # power out / power in = (5 x I) / (v_in x I)
    ok = ["ok" if v_in >= V_OUT + drop else "DROPS OUT" for drop in REGULATORS.values()]
    print(f"{v_in:6.1f} V {heat * 1000:5.0f} mW {heat * THETA:7.1f} C {eff:10.0%}   " + "   ".join(f"{o:>24s}" for o in ok))
print()
print("the old 7805 stops regulating below 7.0 V: Rover's 5 V rail would sag for the last part of every run")
