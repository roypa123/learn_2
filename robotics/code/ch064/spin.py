# spin.py - angular speed and angular acceleration: the turning versions of Chapter 59's equations
import math

# a turntable speeds up from rest to 60 rpm in 2 s
omega_end = 60 * 2 * math.pi / 60            # rpm -> rad/s
alpha = (omega_end - 0) / 2.0                 # angular acceleration, rad/s^2
angle = 0.5 * alpha * 2.0 ** 2                # theta = 1/2 alpha t^2, like s = 1/2 a t^2
print(f"60 rpm = {omega_end:.3f} rad/s, alpha = {alpha:.3f} rad/s^2")
print(f"in 2 s it turns {angle:.3f} rad = {math.degrees(angle):.0f} deg = {angle / (2 * math.pi):.1f} turns")

# points on the turntable at different distances from the centre
for r in [0.05, 0.10, 0.20]:
    print(f"  point {r:.2f} m from the centre: speed {omega_end * r:.3f} m/s, "
          f"sideways (centripetal) acceleration {omega_end ** 2 * r:.2f} m/s^2")

# Rover turns on the spot by 180 deg, with its turn rate limited to 2 rad/s and alpha to 4 rad/s^2
TURN = math.pi
W_MAX, A_MAX = 2.0, 4.0
ramp_angle = W_MAX ** 2 / A_MAX                # speeding up plus slowing down (Chapter 59, in angles)
if TURN >= ramp_angle:
    t = 2 * W_MAX / A_MAX + (TURN - ramp_angle) / W_MAX
else:
    t = 2 * math.sqrt(TURN / A_MAX)
print(f"a 180 deg turn on the spot takes {t:.3f} s")
