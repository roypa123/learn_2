# light_sensor.py - a light-dependent resistor in a divider: choosing the fixed resistor
import math

R_AT_10_LUX = 20000.0      # the LDR's resistance in 10 lux (a dim room)
GAMMA = 0.7                # from the datasheet: R falls as lux^-0.7
V_IN = 5.0


def ldr(lux):
    return R_AT_10_LUX * (lux / 10) ** (-GAMMA)


def v_out(lux, r_fixed):
    """LDR on top, the fixed resistor to ground: brighter light -> less LDR resistance -> higher Vout."""
    return V_IN * r_fixed / (ldr(lux) + r_fixed)


dim, bright = 10, 1000          # the range the robot must tell apart
print(f"LDR: {ldr(dim):.0f} ohm at {dim} lux, {ldr(bright):.0f} ohm at {bright} lux")
print(f"{'fixed R':>9s} {'V at 10 lux':>12s} {'V at 1000 lux':>14s} {'difference':>11s}")
for r in [1000, 2200, 4700, 6800, 10000, 22000, 47000]:
    a, b = v_out(dim, r), v_out(bright, r)
    print(f"{r:7d}   {a:10.3f} V {b:12.3f} V {b - a:9.3f} V")
best = math.sqrt(ldr(dim) * ldr(bright))
print(f"best fixed resistor = sqrt({ldr(dim):.0f} x {ldr(bright):.0f}) = {best:.0f} ohm")
