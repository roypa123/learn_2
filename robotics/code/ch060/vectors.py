# vectors.py - small helper functions for 2D vectors written as (x, y) tuples
import math


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def scale(k, p):
    return (k * p[0], k * p[1])


def length(p):
    return math.hypot(p[0], p[1])


def angle_deg(p):
    return math.degrees(math.atan2(p[1], p[0]))


def from_polar(size, angle_degrees):
    a = math.radians(angle_degrees)
    return (size * math.cos(a), size * math.sin(a))


if __name__ == "__main__":
    v = from_polar(4.66, 59.0)
    print(f"4.66 m/s at 59 deg has parts ({v[0]:.2f}, {v[1]:.2f}) m/s")
    throw = (2.4, 4.0)
    print(f"parts (2.4, 4.0) m/s: size {length(throw):.2f} m/s, angle {angle_deg(throw):.1f} deg")
    air = (0.0, 10.0)
    wind = (3.0, 0.0)
    ground = add(air, wind)
    print(f"air {air} + wind {wind} = ground {ground}, speed {length(ground):.2f} m/s")
    robot, ball = (1.0, 2.0), (4.0, 6.0)
    gap = sub(ball, robot)
    print(f"from robot to ball: {gap}, distance {length(gap):.1f} m")
    print(f"velocity (1.5, 0.5) for 4 s moves the robot by {scale(4, (1.5, 0.5))}")
