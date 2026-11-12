# quantize.py - turning an analog voltage into a number: how fine are the steps?
V_REF = 5.0
signal = 2.4637                  # a sensor's voltage

print(f"true voltage {signal} V")
print(f"{'ADC bits':>9s} {'steps':>7s} {'one step':>10s} {'reading':>8s} {'back to volts':>14s} {'error':>9s}")
for bits in [1, 4, 8, 10, 12, 16]:
    steps = 2 ** bits
    step_v = V_REF / steps
    reading = min(int(signal / step_v), steps - 1)       # the ADC rounds down to a whole step (Chapter 101)
    back = reading * step_v
    print(f"{bits:9d} {steps:7d} {step_v * 1000:7.2f} mV {reading:8d} {back:11.4f} V {(back - signal) * 1000:+7.2f} mV")
print()
print("a 1-bit 'ADC' is just a digital input: above or below the middle")
