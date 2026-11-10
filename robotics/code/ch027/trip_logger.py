# trip_logger.py - record a simulated drive to a CSV file, then read it back
import csv

SETPOINT_M = 0.30
GAIN = 1.0
MAX_SPEED_MS = 0.25
DT_S = 0.5
LOG_FILE = "trip_log.csv"

distance_m = 1.0
time_s = 0.0

with open(LOG_FILE, "w", newline="") as f:      # "w" starts a new, empty file
    writer = csv.writer(f)
    writer.writerow(["time_s", "distance_m", "speed_ms"])     # the header row
    while abs(distance_m - SETPOINT_M) >= 0.01:
        speed_ms = max(-MAX_SPEED_MS, min(MAX_SPEED_MS, GAIN * (distance_m - SETPOINT_M)))
        distance_m -= speed_ms * DT_S
        time_s += DT_S
        writer.writerow([time_s, round(distance_m, 4), round(speed_ms, 4)])

with open(LOG_FILE, newline="") as f:           # no mode means "r": read
    rows = list(csv.DictReader(f))              # a list of dictionaries (Chapter 22)

speeds = [float(row["speed_ms"]) for row in rows]      # everything in a CSV is text
print("rows in the log:", len(rows))
print("first row:", rows[0])
print("top speed:", max(speeds), "m/s")
print("final distance:", rows[-1]["distance_m"], "m at", rows[-1]["time_s"], "s")
