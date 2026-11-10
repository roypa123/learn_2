# sensor_clean.py - clean a list of distance readings and find a value we can trust
MIN_VALID_M = 0.02                  # the sensor's real limits (Chapter 17)
MAX_VALID_M = 4.0

samples = [0.52, 0.51, 0.0, 0.53, 3.91, 0.50, 0.52]   # one dropout (0.0), one spike (3.91)

good = []                           # an empty list to fill
for s in samples:
    if MIN_VALID_M <= s <= MAX_VALID_M:
        good.append(s)              # keep only believable readings

mean_m = sum(good) / len(good)      # the mean (average)
ordered = sorted(good)              # a new, sorted list
median_m = ordered[len(ordered) // 2]   # the value in the middle

print("all readings:", samples)
print("believable:  ", good)
print("sorted:      ", ordered)
print(f"mean   {mean_m:.3f} m")
print(f"median {median_m:.3f} m")
print(f"rejected {len(samples) - len(good)} of {len(samples)} readings")
