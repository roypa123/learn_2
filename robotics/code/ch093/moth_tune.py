# moth_tune.py - Moth's tuning knob: the lower divider resistor sets the light level where the motor starts
from moth_channel import channel, I_START, I_MAX

print(f"{'R_B':>8s} {'starts at':>10s} {'full speed at':>14s} {'steering range':>15s}")
for r_b in [1000, 2200, 4700, 10000, 22000]:
    start = full = None
    lux = 1.0
    while lux < 20000:
        i_c = channel(lux, r_b)[1]
        if start is None and i_c >= I_START:
            start = lux
        if full is None and i_c >= I_MAX - 1e-9:
            full = lux
            break
        lux *= 1.01                    # step up 1% at a time
    print(f"{r_b:6d} ohm {start:7.0f} lux {full:11.0f} lux {full / start:12.1f} x")
print()
print("R_B mostly moves the starting point; the full-speed point is set by the LDR itself (about 2 k ohm)")
