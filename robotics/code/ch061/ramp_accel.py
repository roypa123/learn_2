# ramp_accel.py - can a delivery robot speed up while it climbs a ramp?
import math

G = 9.81
MASS_KG = 25.0
MAX_PUSH_N = 27.5            # 2.2 N m of wheel torque / 0.08 m wheel radius (Chapter 49)
ROLLING_N = 3.0              # rolling resistance, measured by towing the robot slowly

print(" slope   gravity along   spare push   best acceleration   0 to 1 m/s takes")
for percent in [0, 5, 8.33, 10, 12]:
    angle = math.atan(percent / 100)
    gravity_along = MASS_KG * G * math.sin(angle)
    spare = MAX_PUSH_N - gravity_along - ROLLING_N
    if spare > 0:
        a = spare / MASS_KG
        print(f"{percent:5.2f}%   {gravity_along:9.1f} N   {spare:8.1f} N   {a:12.3f} m/s^2   {1.0 / a:10.1f} s")
    else:
        print(f"{percent:5.2f}%   {gravity_along:9.1f} N   {spare:8.1f} N   cannot climb at all")
