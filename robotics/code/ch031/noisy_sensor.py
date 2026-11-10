# noisy_sensor.py - a pretend distance sensor that behaves like a real one
import random
import statistics

random.seed(1)                       # the same "random" numbers on every run


class NoisySensor:
    """Returns the true distance plus noise, with an occasional failed reading."""

    def __init__(self, noise_m=0.01, dropout_chance=0.02):
        self.noise_m = noise_m
        self.dropout_chance = dropout_chance

    def read(self, true_m):
        if random.random() < self.dropout_chance:
            return 0.0                # a failed reading
        return true_m + random.gauss(0, self.noise_m)


sensor = NoisySensor()
readings = [sensor.read(0.50) for _ in range(1000)]
good = [r for r in readings if r > 0.02]

print("first five:", [round(r, 3) for r in readings[:5]])
print(f"failed readings: {len(readings) - len(good)} of {len(readings)}")
print(f"mean  {statistics.mean(good):.4f} m")
print(f"stdev {statistics.stdev(good):.4f} m")

print("histogram:")
for low_cm in range(47, 53):
    count = len([r for r in good if low_cm / 100 <= r < (low_cm + 1) / 100])
    print(f"{low_cm:3d} cm {'#' * (count // 8)} {count}")
