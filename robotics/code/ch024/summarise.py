# summarise.py - one function that returns several facts about a list of readings
def summarise(values):
    """Return (minimum, maximum, mean, median), or None for an empty list."""
    if len(values) == 0:          # a guard: leave early
        return None
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        median = ordered[middle]
    else:
        median = (ordered[middle - 1] + ordered[middle]) / 2
    return ordered[0], ordered[-1], sum(ordered) / len(ordered), median


result = summarise([0.52, 0.51, 0.53, 3.91, 0.50, 0.52])
low, high, mean, median = result
print(f"min {low}  max {high}  mean {mean:.3f}  median {median:.3f}")

result = summarise([])
if result is None:
    print("no readings yet")
