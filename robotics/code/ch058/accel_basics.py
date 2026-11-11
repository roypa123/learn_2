# accel_basics.py - acceleration from a robot's velocity log
times_s = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
velocity = [0.0, 0.5, 1.0, 1.5, 1.5, 1.5, 0.9, 0.3, 0.0]     # m/s

for i in range(1, len(times_s)):
    dv = velocity[i] - velocity[i - 1]
    dt = times_s[i] - times_s[i - 1]
    a = dv / dt
    if a > 0:
        what = "speeding up"
    elif a < 0:
        what = "slowing down"
    else:
        what = "steady speed"
    print(f"{times_s[i - 1]:.0f} s to {times_s[i]:.0f} s:  v {velocity[i - 1]:.1f} -> {velocity[i]:.1f} m/s   a = {a:+.2f} m/s^2   {what}")

distance_m = 0.0
for i in range(1, len(times_s)):
    v_mid = (velocity[i] + velocity[i - 1]) / 2
    distance_m = distance_m + v_mid * (times_s[i] - times_s[i - 1])
print(f"distance travelled: {distance_m:.2f} m")
print(f"largest acceleration as a share of g: {0.5 / 9.81:.3f} g")
