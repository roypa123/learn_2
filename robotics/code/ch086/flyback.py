# flyback.py - switch off a 24 V valve coil: a plain diode is gentle but slow, a diode plus Zener is fast
V = 24.0
R = 48.0                 # a 24 V, 0.5 A solenoid valve
L = 0.10                 # henries
DT = 1e-6
I0 = V / R


def release(clamp_v):
    """After switch-off the coil's current flows through the clamp: the voltage across the inductance is -(I R + clamp)."""
    i, t, peak = I0, 0.0, 0.0
    while i > 0.01 * I0:                 # until the current is down to 1%
        v_l = -(i * R + clamp_v)
        i = max(i + v_l / L * DT, 0.0)
        t += DT
    return t, V + clamp_v                # the switch sees the supply plus the clamp voltage


print(f"valve coil: {V:.0f} V, {R:.0f} ohm, {L} H, current {I0:.2f} A, energy {0.5 * L * I0 ** 2 * 1000:.1f} mJ")
print(f"{'catching the current with':32s} {'switch sees':>12s} {'current gone (1%) after':>25s}")
for name, clamp in [("plain diode (0.7 V)", 0.7), ("diode + 12 V Zener", 12.7), ("diode + 24 V Zener", 24.7), ("diode + 33 V Zener", 33.7)]:
    t, vsw = release(clamp)
    print(f"{name:32s} {vsw:9.1f} V {t * 1000:18.2f} ms")
print()
print("a switch rated 60 V is safe with all of these; the Zener ones release the valve up to 5 times faster")
