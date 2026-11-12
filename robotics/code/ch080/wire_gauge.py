# wire_gauge.py - American Wire Gauge (AWG) sizes: diameter, area, resistance and a safe current
import math

RHO = 1.68e-8
HEAT_LIMIT_W_PER_M = 5.0           # half of Chapter 76's 10 W/m, for wires bundled inside a robot


def awg_diameter_mm(n):
    """The AWG formula: each gauge number down makes the wire 1.123 times thicker."""
    return 0.127 * 92 ** ((36 - n) / 39)


print(f"{'AWG':>4s} {'diameter':>9s} {'area':>9s} {'mohm/m':>8s} {'safe A':>7s}  typical robot use")
uses = {30: "wire-wrap, inside sensors", 26: "thin signal wires", 24: "breadboard jumpers, servo leads",
        22: "signal and small power wires (Rover)", 20: "Rover's battery and motor wires",
        18: "small robot power", 16: "4 A to 15 A power", 14: "drone power board",
        12: "drone battery lead (40 A)", 10: "large drone, humanoid battery"}
for n in [30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10]:
    d = awg_diameter_mm(n)
    area = math.pi * (d / 2) ** 2                       # mm^2
    r = RHO / (area * 1e-6) * 1000                       # milliohms per metre
    safe = math.sqrt(HEAT_LIMIT_W_PER_M / (r / 1000))    # I = sqrt(P / R) for 1 m
    print(f"{n:4d} {d:7.3f} mm {area:6.3f} mm2 {r:8.1f} {safe:7.1f}  {uses.get(n, '')}")

print()
print("rule of thumb: 3 gauge numbers down = twice the area = half the resistance")
print(f"  AWG 20 / AWG 23 area ratio: {(awg_diameter_mm(20) / awg_diameter_mm(23)) ** 2:.3f}")
