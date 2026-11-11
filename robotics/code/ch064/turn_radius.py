# turn_radius.py - a two-wheeled robot turns by driving its wheels at different speeds
TRACK_M = 0.15           # distance between Rover's wheels (Chapter 46)


def body_motion(v_left, v_right):
    """Forward speed, turn rate and turning radius from the two wheel speeds."""
    v = (v_left + v_right) / 2
    omega = (v_right - v_left) / TRACK_M          # anticlockwise is positive
    radius = v / omega if omega != 0 else float("inf")
    return v, omega, radius


def wheels_for(v, radius):
    """Wheel speeds to drive at v around a circle of the given radius (positive = turning left)."""
    omega = v / radius
    return v - omega * TRACK_M / 2, v + omega * TRACK_M / 2


for left, right in [(0.30, 0.30), (0.225, 0.375), (0.20, 0.40), (0.0, 0.30), (-0.15, 0.15)]:
    v, w, R = body_motion(left, right)
    print(f"wheels L {left:+.3f} R {right:+.3f} m/s -> v {v:.3f} m/s, omega {w:+.2f} rad/s, radius {R:.3f} m")

print("to drive at 0.4 m/s round a corner:")
for radius in [2.0, 0.5, 0.2, 0.075]:
    l, r = wheels_for(0.4, radius)
    print(f"  radius {radius:5.3f} m: left {l:.3f} m/s, right {r:.3f} m/s")
