# pwm_motor.py - the current in a small DC motor driven by PWM: how much does it ripple at each frequency?
# The motor is a resistor and an inductor in series (Chapter 85); the current cannot jump, it follows
# di/dt = (v - R*i) / L. The motor is held still here (a stall), so no back-voltage: the worst case.
R = 15.0                    # ohms: the small motor of Chapter 87
L = 0.002                   # henries: 2 mH, a typical small DC motor
V = 6.0                     # volts from the battery
DUTY = 0.5                  # half on, half off

tau = L / R
print(f"motor time constant L/R = {tau * 1000:.3f} ms; average current {V * DUTY / R * 1000:.0f} mA")
print(f"{'PWM frequency':>14s} {'period':>9s} {'lowest':>8s} {'highest':>8s} {'ripple':>8s}")
for freq in [100, 490, 980, 4000, 20000]:
    period = 1 / freq
    dt = period / 2000                       # 2,000 small Euler steps per period (Chapter 71)
    i = 0.0
    lows, highs = [], []
    for cycle in range(60):                  # run 60 periods so the current settles
        lo, hi = 1e9, -1e9
        for step in range(2000):
            v = V if step < 2000 * DUTY else 0.0     # on for the first half of each period
            i += (v - R * i) / L * dt
            lo, hi = min(lo, i), max(hi, i)
        lows.append(lo)
        highs.append(hi)
    lo, hi = lows[-1], highs[-1]
    print(f"{freq:11d} Hz {period * 1000:7.3f} ms {lo * 1000:6.0f} mA {hi * 1000:6.0f} mA {(hi - lo) * 1000:6.0f} mA")
