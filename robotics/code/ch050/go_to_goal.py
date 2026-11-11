# go_to_goal.py - Rover turns towards a goal with atan2 and a wrapped heading error
import math


def wrap_pi(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


GOAL = (-2.0, -1.0)
SPEED = 0.3            # m/s
TURN_GAIN = 2.0        # rad/s of turning for each rad of error
DT = 0.1               # seconds per step

x, y, heading = 0.0, 0.0, math.radians(30)
path = [(x, y)]
for step in range(200):
    dx = GOAL[0] - x
    dy = GOAL[1] - y
    distance = math.hypot(dx, dy)
    if distance < 0.05:
        break
    wanted = math.atan2(dy, dx)
    error = wrap_pi(wanted - heading)
    heading = wrap_pi(heading + TURN_GAIN * error * DT)
    x += SPEED * math.cos(heading) * DT
    y += SPEED * math.sin(heading) * DT
    path.append((x, y))
    if step in (0, 1, 2):
        print(f"step {step}: wanted {math.degrees(wanted):7.1f} deg, error {math.degrees(error):7.1f} deg")

print(f"reached ({x:.3f}, {y:.3f}) after {step} steps = {step * DT:.1f} s")
