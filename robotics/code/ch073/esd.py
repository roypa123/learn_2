# esd.py - static electricity on a person: charge, energy, and the current when it jumps into a chip
import math

ELECTRON_C = 1.602e-19
BODY_F = 100e-12            # a person stores charge like a 100 pF capacitor (Chapter 84 explains farads)
BODY_OHM = 1500             # the body's resistance in the standard test model
STRAP_OHM = 1e6             # the resistor inside a wrist strap

print(f"{'volts on the body':>18s} {'charge':>10s} {'electrons':>11s} {'energy':>10s} {'peak current':>13s}")
for volts in [100, 1500, 3000, 15000]:
    charge = BODY_F * volts                     # Q = C x V
    energy = 0.5 * BODY_F * volts ** 2          # the energy stored, joules
    peak = volts / BODY_OHM                     # the first instant of the spark, amps
    print(f"{volts:15d} V {charge * 1e9:8.1f} nC {charge / ELECTRON_C:11.2e} {energy * 1000:8.3f} mJ {peak:10.2f} A")

print()
print("you feel a spark from about 3,000 V; a chip can die from 100 V")
tau = STRAP_OHM * BODY_F
print(f"wrist strap: time constant R x C = {tau * 1e6:.0f} microseconds")
for t_us in [0, 100, 300, 500]:
    v = 15000 * math.exp(-t_us * 1e-6 / tau)
    print(f"  after {t_us:3d} microseconds: {v:8.1f} V left")
