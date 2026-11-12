# wire_gauge.py - which wire thickness for each of Rover's connections?
import math

RHO_COPPER = 1.68e-8          # resistivity of copper, ohm metre


def awg_diameter_mm(awg):
    """The American Wire Gauge formula: every 6 gauges halves the diameter (roughly)."""
    return 0.127 * 92 ** ((36 - awg) / 39)


def ohm_per_m(awg):
    d = awg_diameter_mm(awg) / 1000
    area = math.pi * d ** 2 / 4
    return RHO_COPPER / area


print(f"{'AWG':>4s} {'diameter':>9s} {'ohm per m':>10s}")
for awg in [30, 26, 24, 22, 20, 18, 16]:
    print(f"{awg:4d} {awg_diameter_mm(awg):6.3f} mm {ohm_per_m(awg):10.4f}")
print()

# Rover's wires: name, current (A), one-way length (m); there and back makes the loop twice as long
WIRES = [("battery to motor driver", 3.1, 0.25), ("driver to one motor", 1.5, 0.20),
         ("5 V rail to sensors", 0.19, 0.30), ("signal wire (UART)", 0.002, 0.15)]
print(f"{'wire':25s} {'amps':>6s}  thinnest gauge with under 0.1 V drop and under 0.5 W per metre")
for name, amps, length in WIRES:
    for awg in [30, 26, 24, 22, 20, 18, 16]:
        drop = amps * ohm_per_m(awg) * 2 * length            # Ohm's law over the loop (Chapter 75)
        heat_per_m = amps ** 2 * ohm_per_m(awg)              # I^2 R for one metre (Chapter 76)
        if drop < 0.1 and heat_per_m < 0.5:
            print(f"{name:25s} {amps:6.3f}  AWG {awg}: drop {drop * 1000:5.1f} mV, {heat_per_m:5.3f} W/m")
            break
