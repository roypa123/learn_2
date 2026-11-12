# jitter_compare.py - a model of how late a 100 Hz control loop starts on a microcontroller and on a Linux computer
import random

random.seed(94)
LOOPS = 10_000                  # 100 seconds of loops at 100 Hz
SPEED = 0.5                     # Rover drives at 0.5 m/s


def late_mcu():
    return abs(random.gauss(0, 0.002))                    # ms: only a few microseconds, every time


def late_linux():
    late = abs(random.gauss(0, 0.05))                     # usually 50 microseconds or so
    if random.random() < 0.01:                            # but about 1 loop in 100, the system is busy
        late += random.uniform(1, 20)                     # (writing a file, Wi-Fi, another program)
    return late


for name, late in [("microcontroller", late_mcu), ("Linux computer", late_linux)]:
    times = sorted(late() for _ in range(LOOPS))
    middle, p99, worst = times[LOOPS // 2], times[int(LOOPS * 0.99)], times[-1]
    print(f"{name:16s} late by: typical {middle:6.3f} ms, 1 in 100 over {p99:6.3f} ms, worst {worst:6.2f} ms"
          f"  -> worst extra drive {worst / 1000 * SPEED * 1000:5.1f} mm")
