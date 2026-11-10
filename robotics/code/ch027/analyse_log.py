# analyse_log.py - after a test drive: what actually happened?
import csv

times = []
speeds = []
volts = []
bumps = 0
previous_bumper = 0

with open("drive_log.csv", newline="") as f:
    for row in csv.DictReader(f):
        times.append(float(row["time_s"]))
        speeds.append(float(row["speed_ms"]))
        volts.append(float(row["battery_v"]))
        bumper = int(row["bumper"])
        if bumper == 1 and previous_bumper == 0:     # count only the moment it goes on
            bumps += 1
        previous_bumper = bumper

distance_m = 0.0
for i in range(len(times) - 1):
    dt = times[i + 1] - times[i]
    distance_m += (speeds[i] + speeds[i + 1]) / 2 * dt   # average speed x time

print(f"duration:   {times[-1] - times[0]:.1f} s")
print(f"distance:   {distance_m:.2f} m")
print(f"top speed:  {max(speeds):.2f} m/s")
print(f"lowest V:   {min(volts):.2f} V at t = {times[volts.index(min(volts))]:.1f} s")
print(f"bumps:      {bumps}")
