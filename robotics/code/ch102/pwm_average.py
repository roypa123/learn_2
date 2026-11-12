# pwm_average.py - what analogWrite values mean: duty cycle, on-time, and the average voltage
V = 5.0
FREQ = 490.0                          # Hz: the PWM frequency on Uno pins 3, 9, 10 and 11
period_ms = 1000 / FREQ

print(f"PWM at {FREQ:.0f} Hz: one period = {period_ms:.2f} ms")
print(f"{'value':>6s} {'duty':>7s} {'on for':>8s} {'average':>8s}")
for value in [0, 1, 64, 128, 191, 254, 255]:
    duty = value / 255                # analogWrite's 0-255 is the share of each period that the pin is HIGH
    print(f"{value:6d} {duty * 100:6.1f}% {duty * period_ms:6.3f} ms {duty * V:7.2f} V")
