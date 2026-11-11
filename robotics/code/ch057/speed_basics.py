# speed_basics.py - average speed, average velocity, and changing units
times_s = [0.0, 2.0, 5.0, 7.0, 9.0, 10.0, 12.0]
positions_m = [0.0, 2.0, 5.0, 5.0, 3.0, 1.5, 4.0]

distance_m = 0.0
for i in range(1, len(positions_m)):
    dt = times_s[i] - times_s[i - 1]
    dx = positions_m[i] - positions_m[i - 1]
    distance_m = distance_m + abs(dx)
    print(f"{times_s[i - 1]:4.1f} s to {times_s[i]:4.1f} s:  velocity {dx / dt:+5.2f} m/s   speed {abs(dx) / dt:4.2f} m/s")

total_time_s = times_s[-1] - times_s[0]
displacement_m = positions_m[-1] - positions_m[0]
avg_speed = distance_m / total_time_s
avg_velocity = displacement_m / total_time_s
print(f"average speed:    {distance_m:.1f} m / {total_time_s:.0f} s = {avg_speed:.3f} m/s = {avg_speed * 3.6:.2f} km/h")
print(f"average velocity: {displacement_m:+.1f} m / {total_time_s:.0f} s = {avg_velocity:+.3f} m/s")
