# noise_compare.py - send a value over a noisy wire, as an analog voltage and as digital bits
import random

random.seed(5)
V = 5.0
TRUE_VALUE = 0.62                 # the sensor's reading: 62% of full scale
BITS = 8

# analog: the value is the voltage itself; every bit of noise becomes an error
# digital: the value is sent as 8 bits, each 0 V or 5 V; noise only matters if it crosses the 2.5 V decision line
code = round(TRUE_VALUE * (2 ** BITS - 1))
bits = [(code >> k) & 1 for k in range(BITS)]

print(f"value to send: {TRUE_VALUE:.3f} (digital code {code} = {''.join(str(b) for b in reversed(bits))})")
print(f"{'noise (V)':>10s} {'analog received':>16s} {'analog error':>13s} {'digital received':>17s} {'bit errors':>11s}")
for noise in [0.05, 0.2, 0.5, 1.0, 2.0, 3.0]:
    a = (TRUE_VALUE * V + random.gauss(0, noise)) / V
    rx_bits = [1 if b * V + random.gauss(0, noise) > V / 2 else 0 for b in bits]
    errors = sum(1 for b, r in zip(bits, rx_bits) if b != r)
    rx = sum(r << k for k, r in enumerate(rx_bits)) / (2 ** BITS - 1)
    print(f"{noise:10.2f} {a:16.3f} {a - TRUE_VALUE:+13.3f} {rx:17.3f} {errors:11d}")
print()
print("small noise: analog is slightly wrong, digital is exactly right (the error is only the 1/255 step)")
print("huge noise: both fail; digital fails suddenly, and checksums (Chapter 533) can at least detect it")
