# aliasing.py - sample a fast 50 Hz hum too slowly and it pretends to be a slow wave
import math

F_SIGNAL = 50.0                 # mains hum picked up by a sensor wire, Hz

print("sampling the 50 Hz hum 45 times a second (first 10 samples):")
for k in range(10):
    t = k / 45.0
    print(f"  t = {t:.3f} s   value = {math.sin(2 * math.pi * F_SIGNAL * t):+.3f}")
print()

print(f"{'samples per second':>19s} {'what the samples seem to show':>32s}")
for fs in [45, 60, 90, 110, 1000]:
    alias = abs(F_SIGNAL - round(F_SIGNAL / fs) * fs)      # the nearest whole number of sampling rates
    note = "the true 50 Hz" if fs > 2 * F_SIGNAL else "a FALSE wave"
    print(f"{fs:19d} {alias:24.0f} Hz   {note}")
