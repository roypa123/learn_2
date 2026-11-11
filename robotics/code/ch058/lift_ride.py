# lift_ride.py - turn a phone's accelerometer log from a lift ride into velocity and height
import random

DT_S = 0.05                                   # 20 readings per second
random.seed(1)


def true_accel(t):
    """The lift's real acceleration (m/s^2): speed up, cruise, slow down."""
    if t < 2.0:
        return 1.0
    if t < 8.0:
        return 0.0
    if t < 10.0:
        return -1.0
    return 0.0


readings = []
for k in range(0, 241):                       # 12 seconds
    t = k * DT_S
    readings.append(true_accel(t) + random.gauss(0, 0.05) + 0.02)   # noise plus a small fixed error

velocity = 0.0
height = 0.0
top_speed = 0.0
for k, a in enumerate(readings):
    velocity = velocity + a * DT_S
    height = height + velocity * DT_S
    top_speed = max(top_speed, velocity)
    if k % 40 == 0:
        print(f"t = {k * DT_S:4.1f} s   a = {a:+5.2f} m/s^2   v = {velocity:5.2f} m/s   height = {height:5.2f} m")

print(f"top speed {top_speed:.2f} m/s, final speed {velocity:.2f} m/s, height {height:.1f} m")
print("true values: top speed 2.00 m/s, final speed 0.00 m/s, height 16.0 m")
