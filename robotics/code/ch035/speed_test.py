# speed_test.py - the same sum, done with a Python loop and with NumPy
import time

import numpy as np

N = 1_000_000

start = time.perf_counter()
total = 0.0
for i in range(N):
    total += i * i * 0.5
loop_s = time.perf_counter() - start

start = time.perf_counter()
values = np.arange(N, dtype=float)
numpy_total = np.sum(values * values * 0.5)
numpy_s = time.perf_counter() - start

print(f"loop:  {total:.6e} in {loop_s * 1000:7.1f} ms")
print(f"numpy: {numpy_total:.6e} in {numpy_s * 1000:7.1f} ms")
print(f"numpy was {loop_s / numpy_s:.0f} times faster")
