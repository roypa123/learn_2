# drone_wire.py - how thick must the wire from a drone battery to its motors be?
RHO_COPPER = 1.68e-8
LENGTH = 1.0            # 0.5 m out and 0.5 m back
CURRENT = 40.0          # all four motors at full power
PACK_V = 14.8
MAX_LOSS = 0.2          # we allow 0.2 V of loss in the wire

print(f"{'area':>8s} {'ohms':>8s} {'lost volts':>11s} {'share':>7s} {'ok?':>5s}")
for area in [0.5, 1.0, 2.0, 4.0, 6.0]:
    r = RHO_COPPER * LENGTH / (area * 1e-6)
    lost = CURRENT * r
    ok = "yes" if lost <= MAX_LOSS else "no"
    print(f"{area:5.1f} mm2 {r:8.4f} {lost:11.2f} {lost / PACK_V:7.1%} {ok:>5s}")

print()
r_max = MAX_LOSS / CURRENT                               # R = V / I
area_min = RHO_COPPER * LENGTH / r_max * 1e6             # A = rho L / R, in mm2
print(f"to lose at most {MAX_LOSS} V at {CURRENT} A, R must be under {r_max * 1000:.1f} milliohms")
print(f"so the wire needs at least {area_min:.2f} mm2: choose 4 mm2 (about 12 AWG)")
