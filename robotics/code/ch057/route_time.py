# route_time.py - how long a delivery robot's route takes when each part has its own speed limit
route = [
    ("pavement", 400.0, 1.6),        # (name, length in m, speed in m/s)
    ("crossing", 15.0, 1.0),
    ("market street", 120.0, 0.6),
    ("pavement", 250.0, 1.6),
    ("building lobby", 30.0, 0.4),
]

total_m = 0.0
total_s = 0.0
for name, length_m, speed in route:
    part_s = length_m / speed
    total_m = total_m + length_m
    total_s = total_s + part_s
    print(f"{name:15s} {length_m:6.0f} m at {speed:.1f} m/s  ->  {part_s:6.1f} s")

speeds = [speed for name, length_m, speed in route]
print(f"total: {total_m:.0f} m in {total_s:.1f} s ({total_s / 60:.1f} min)")
print(f"true average speed:        {total_m / total_s:.3f} m/s")
print(f"average of the 5 limits:   {sum(speeds) / len(speeds):.3f} m/s  (wrong way to average)")
