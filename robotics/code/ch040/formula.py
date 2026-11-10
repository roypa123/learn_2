# formula.py - one rule written with letters works for every robot
def trip_time_s(distance_m, speed_ms, stops, stop_s):
    return distance_m / speed_ms + stops * stop_s


print("robot     distance  speed  stops  stop time  total time")
robots = [
    ("Rover", 12, 0.4, 2, 5),
    ("Courier", 800, 1.2, 4, 30),
    ("Mower", 450, 0.5, 0, 0),
]
for name, d, v, n, s in robots:
    t = trip_time_s(d, v, n, s)
    print(f"{name:<9} {d:8d} {v:6.1f} {n:6d} {s:10d} {t:9.1f} s")
