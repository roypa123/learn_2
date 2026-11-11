# series_parallel.py - combining resistors: in series they add, in parallel their reciprocals add
def series(resistors):
    """Total resistance of resistors in a row: just add them."""
    return sum(resistors)


def parallel(resistors):
    """Total resistance of resistors side by side: 1 / (1/R1 + 1/R2 + ...)."""
    return 1 / sum(1 / r for r in resistors)


cases = [
    ("two 100 ohm", [100, 100]),
    ("100 and 300 ohm", [100, 300]),
    ("10 and 1000 ohm", [10, 1000]),
    ("four 1 kohm", [1000, 1000, 1000, 1000]),
    ("Rover's two stalled motors (4.8 ohm each)", [4.8, 4.8]),
    ("motor 4.8 + wire 0.01 + battery inside 0.15", [4.8, 0.01, 0.15]),
]
print(f"{'resistors':46s} {'series':>10s} {'parallel':>10s}")
for name, rs in cases:
    print(f"{name:46s} {series(rs):10.3f} {parallel(rs):10.3f}")

print()
print("n equal resistors of R in parallel give R / n:")
for n in [1, 2, 3, 4, 10]:
    print(f"  {n:2d} x 1000 ohm in parallel = {parallel([1000] * n):7.1f} ohm")
