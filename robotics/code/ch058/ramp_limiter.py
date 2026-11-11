# ramp_limiter.py - stop a velocity command from changing faster than a safe acceleration
DT_S = 0.1              # the loop runs 10 times a second
MAX_ACCEL = 0.8         # m/s^2, found by testing the robot with its load
MAX_DECEL = 1.2         # m/s^2, braking may be a little harder


def limit_step(current, wanted):
    """Move the velocity towards the wanted value, but by no more than one loop's allowed change."""
    if abs(wanted) > abs(current) and wanted * current >= 0:
        max_change = MAX_ACCEL * DT_S       # getting faster
    else:
        max_change = MAX_DECEL * DT_S       # getting slower, or changing direction
    change = wanted - current
    if change > max_change:
        change = max_change
    elif change < -max_change:
        change = -max_change
    return current + change


v = 0.0
for step in range(0, 41):
    t = step * DT_S
    wanted = 1.6 if t < 2.5 else 0.0      # the planner asks for full speed, then a stop
    if step % 4 == 0:
        print(f"t = {t:3.1f} s   wanted {wanted:3.1f} m/s   sent to motors {v:4.2f} m/s")
    v = limit_step(v, wanted)
