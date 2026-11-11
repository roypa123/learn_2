# estimate_pi.py - throw random points at a square and count those inside the circle
import math
import random

random.seed(3)

for throws in [100, 1_000, 10_000, 100_000, 1_000_000]:
    inside = 0
    for _ in range(throws):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            inside += 1
    estimate = 4 * inside / throws
    print(f"{throws:9d} throws: pi is about {estimate:.4f}  (error {abs(estimate - math.pi):.4f})")
