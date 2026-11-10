# average_helps.py - how much does averaging N readings reduce the noise?
import random
import statistics

random.seed(2)
NOISE_M = 0.01

for n in (1, 4, 16, 64):
    averages = []
    for _ in range(2000):                # repeat the experiment many times
        samples = [0.50 + random.gauss(0, NOISE_M) for _ in range(n)]
        averages.append(sum(samples) / n)
    spread = statistics.stdev(averages)
    print(f"average of {n:2d}: spread {spread * 1000:5.2f} mm   predicted {NOISE_M / n ** 0.5 * 1000:5.2f} mm")
