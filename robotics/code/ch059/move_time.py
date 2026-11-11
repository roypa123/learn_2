# move_time.py - how long a point-to-point move takes when the robot must speed up and slow down
import math


def move_time(distance, v_max, accel):
    """Time to move `distance` from rest to rest, with top speed v_max and acceleration accel."""
    ramp_distance = v_max ** 2 / accel          # speeding up plus slowing down, each v_max^2 / (2 accel)
    if distance >= ramp_distance:
        cruise = distance - ramp_distance       # a trapezoid: speed up, cruise, slow down
        return 2 * v_max / accel + cruise / v_max, v_max
    v_peak = math.sqrt(accel * distance)        # a triangle: never reaches v_max
    return 2 * v_peak / accel, v_peak


L, GRIP_S, ACCEL = 0.6, 0.3, 6.0
for v_max in [1.5, 3.0]:
    t_move, v_top = move_time(L, v_max, ACCEL)
    cycle = 2 * t_move + 2 * GRIP_S
    print(f"v_max {v_max} m/s: one move {t_move:.3f} s (top speed reached {v_top:.2f} m/s), "
          f"cycle {cycle:.3f} s, {3600 / cycle:.0f} parts per hour")
print(f"ignoring acceleration (Chapter 40): one move {L / 1.5:.3f} s, cycle {2 * L / 1.5 + 2 * GRIP_S:.3f} s")
