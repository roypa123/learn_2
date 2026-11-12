# rc_filter.py - an RC filter on a noisy sensor wire: less noise, but a little delay
import math
import random

random.seed(3)
R = 10_000.0
C = 1e-6
TAU = R * C                    # 10 ms
DT = 1e-5                      # 10 microsecond steps
NOISE_V = 0.4                  # motor noise picked up by the wire, peak (a 2 kHz buzz plus random spikes)

v_cap, t = 0.0, 0.0
raw_dev, filt_dev = [], []
rise_time = None
while t < 0.15:
    true = 1.0 if t < 0.05 else 2.0                       # the sensor's real output steps from 1 V to 2 V at 50 ms
    raw = true + NOISE_V * math.sin(2 * math.pi * 2000 * t) + random.uniform(-0.1, 0.1)
    v_cap = v_cap + (raw - v_cap) / TAU * DT              # the capacitor's voltage follows the input, slowly
    t += DT
    if 0.03 < t < 0.05:
        raw_dev.append(abs(raw - true))
        filt_dev.append(abs(v_cap - true))
    if rise_time is None and t > 0.05 and v_cap >= 1.9:
        rise_time = t - 0.05
print(f"RC = {TAU * 1000:.0f} ms, corner frequency 1 / (2 pi R C) = {1 / (2 * math.pi * TAU):.1f} Hz")
print(f"noise before the filter: average {sum(raw_dev) / len(raw_dev) * 1000:.0f} mV, worst {max(raw_dev) * 1000:.0f} mV")
print(f"noise after the filter:  average {sum(filt_dev) / len(filt_dev) * 1000:.1f} mV, worst {max(filt_dev) * 1000:.1f} mV")
print(f"the price: after a real step, the output takes {rise_time * 1000:.0f} ms to reach 90% of it")
