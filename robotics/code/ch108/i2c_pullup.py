# i2c_pullup.py - choose the I2C pull-up resistors
# A chip pulls a line LOW with a transistor; only the pull-up resistor pulls it HIGH again, charging
# the bus's capacitance (wires + chip pins). The rise from 30 % to 70 % of the supply takes
# about 0.85 x R x C (Chapter 84), and the I2C standard allows at most 1000 ns at 100 kHz and
# 300 ns at 400 kHz. The resistor must also not be so small that a chip cannot pull it LOW:
# chips must sink 3 mA while holding the line at 0.4 V or less.
V = 5.0
R_MIN = (V - 0.4) / 0.003                         # smallest pull-up allowed at 5 V
print(f"at {V} V the pull-up must be at least {R_MIN:.0f} ohm (3 mA through it at 0.4 V)")
print(f"{'bus capacitance':>16s} | {'4.7 k: rise time':>16s} | {'largest R for 100 kHz':>21s} | {'largest R for 400 kHz':>21s}")
for c_pf in [50, 100, 200, 400]:
    c = c_pf * 1e-12
    rise_47k = 0.8473 * 4700 * c * 1e9            # nanoseconds
    r100 = 1000e-9 / (0.8473 * c)
    r400 = 300e-9 / (0.8473 * c)
    print(f"{c_pf:13d} pF | {rise_47k:13.0f} ns | {r100 / 1000:18.1f} k | {r400 / 1000:18.1f} k")
