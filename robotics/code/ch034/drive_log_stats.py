# drive_log_stats.py - load a whole log into one 2-D array and study its columns
from pathlib import Path

import numpy as np

log_path = Path(__file__).parent.parent / "ch027" / "drive_log.csv"
data = np.loadtxt(log_path, delimiter=",", skiprows=1)    # skip the header row

print("shape:", data.shape)                  # rows, columns
t = data[:, 0]                               # every row, column 0
speed = data[:, 1]
volts = data[:, 2]

dt = np.diff(t)                              # the differences between neighbours
mean_speed = (speed[:-1] + speed[1:]) / 2    # the average of each neighbouring pair
distance = np.sum(mean_speed * dt)           # the trapezoid rule of Chapter 27

print(f"distance: {distance:.2f} m")
print(f"lowest voltage: {volts.min():.2f} V at t = {t[volts.argmin()]:.1f} s")
print(f"rows at full speed: {np.sum(speed >= 0.25)}")
print("mean of each column:", data.mean(axis=0).round(3))
