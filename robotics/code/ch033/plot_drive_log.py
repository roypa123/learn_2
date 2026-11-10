# plot_drive_log.py - turn the Chapter 27 log file into a two-part graph
import csv
from pathlib import Path

import matplotlib.pyplot as plt

log_path = Path(__file__).parent.parent / "ch027" / "drive_log.csv"

times, speeds, volts = [], [], []
with open(log_path, newline="") as f:
    for row in csv.DictReader(f):
        times.append(float(row["time_s"]))
        speeds.append(float(row["speed_ms"]))
        volts.append(float(row["battery_v"]))

fig, (top, bottom) = plt.subplots(2, 1, figsize=(8, 5), sharex=True)

top.step(times, speeds, where="post", color="green")
top.set_ylabel("speed (m/s)")
top.set_title("Test drive")
top.grid(True)

bottom.plot(times, volts, "o-", color="tab:blue")
bottom.axhline(6.0, color="red", linestyle=":", label="minimum 6.0 V")
bottom.set_xlabel("time (s)")
bottom.set_ylabel("battery (V)")
bottom.legend()
bottom.grid(True)

fig.tight_layout()
fig.savefig("drive_log.png", dpi=150)
print("saved drive_log.png from", len(times), "rows")
