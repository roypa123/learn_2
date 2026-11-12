# rc_filter.py - smooth a PWM signal into a steady voltage with a resistor and a capacitor (Chapter 84)
V = 5.0
FREQ = 490.0
DUTY = 128 / 255                       # analogWrite(pin, 128)
STEPS = 400                            # small time steps per PWM period

for r, c in [(1000, 1e-6), (10000, 1e-6), (10000, 10e-6)]:
    tau = r * c                                          # the time constant (Chapter 84)
    dt = 1 / FREQ / STEPS
    v = 0.0
    for cycle in range(int(8 * tau * FREQ) + 20):        # run for more than 8 time constants: fully settled
        lo, hi = 1e9, -1e9
        for k in range(STEPS):
            v_in = V if k < STEPS * DUTY else 0.0        # the PWM pin: HIGH for the first half of each period
            v += (v_in - v) / tau * dt                   # the capacitor charges towards the input
            lo, hi = min(lo, v), max(hi, v)
    print(f"R {r:6d} ohm, C {c * 1e6:4.0f} uF: tau {tau * 1000:6.1f} ms, average {(lo + hi) / 2:.2f} V, "
          f"ripple {(hi - lo) * 1000:6.1f} mV, reaches 95% in about {3 * tau * 1000:5.0f} ms")
