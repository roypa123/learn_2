# rc_charge.py - a capacitor charging through a resistor: simulate it in small steps, compare with the exact curve
import math

V_SUPPLY = 5.0
R = 10_000.0          # ohms
C = 100e-6            # farads (100 microfarads)
TAU = R * C           # the time constant, seconds
DT = TAU / 1000

print(f"R = {R:.0f} ohm, C = {C * 1e6:.0f} uF, time constant RC = {TAU:.3f} s")
v, t = 0.0, 0.0
marks = [1, 2, 3, 5]
print(f"{'time':>8s} {'simulated':>10s} {'exact':>8s} {'% of 5 V':>9s}")
while marks:
    i = (V_SUPPLY - v) / R          # Ohm's law: the resistor's current depends on the gap still to fill
    v = v + i / C * DT              # the capacitor's voltage rises by (charge added) / C
    t = t + DT
    if t >= marks[0] * TAU - DT / 2:
        exact = V_SUPPLY * (1 - math.exp(-t / TAU))
        print(f"{marks[0]:4d} RC  {v:8.3f} V {exact:6.3f} V {v / V_SUPPLY:8.1%}")
        marks.pop(0)

print()
print("discharging the same capacitor from 5 V through the same resistor:")
for n in [1, 2, 3, 5]:
    print(f"  after {n} RC = {n * TAU:.0f} s: {V_SUPPLY * math.exp(-n):.3f} V ({math.exp(-n):.1%} left)")
