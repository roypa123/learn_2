# sensor_array.py - the same sensor cleaning as Chapter 21, now with a NumPy array
import numpy as np

MIN_VALID_M, MAX_VALID_M = 0.02, 4.0

samples = np.array([0.52, 0.51, 0.0, 0.53, 3.91, 0.50, 0.52])

valid = (samples >= MIN_VALID_M) & (samples <= MAX_VALID_M)     # True or False for each item
good = samples[valid]                                           # keep only the True ones

print("valid:  ", valid)
print("good:   ", good)
print("in cm:  ", good * 100)
print(f"mean   {good.mean():.3f} m")
print(f"median {np.median(good):.3f} m")
print(f"rejected {samples.size - good.size} of {samples.size}")
