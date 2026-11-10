# cycle_time.py - T = 2L/v + 2g for a pick-and-place arm
def cycle_time_s(length_m, speed_ms, grip_s):
    return 2 * length_m / speed_ms + 2 * grip_s


LENGTH_M = 0.6
GRIP_S = 0.3

print("speed (m/s)  cycle (s)  parts per hour")
for speed in [0.75, 1.5, 3.0, 6.0]:
    cycle = cycle_time_s(LENGTH_M, speed, GRIP_S)
    per_hour = 3600 / cycle
    print(f"{speed:11.2f} {cycle:10.2f} {per_hour:15.0f}")
