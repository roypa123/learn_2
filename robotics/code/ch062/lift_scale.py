# lift_scale.py - what a bathroom scale (or a robot's force sensor) reads in a moving lift
G = 9.81
MASS_KG = 30.0               # a robot standing on the scale


def lift_accel(t):
    """The lift's acceleration in m/s^2, up is positive: speed up, cruise, slow down (Chapter 58)."""
    if t < 2.0:
        return 1.0
    if t < 8.0:
        return 0.0
    if t < 10.0:
        return -1.0
    return 0.0


print("  t (s)   lift a (m/s^2)   scale reads (N)   looks like (kg)")
for t in [1.0, 5.0, 9.0, 11.0]:
    a = lift_accel(t)
    reading = MASS_KG * (G + a)        # the scale pushes up: N - m g = m a
    print(f"{t:6.1f}   {a:+12.1f}   {reading:15.1f}   {reading / G:13.1f}")
print(f"in free fall (cable cut), a = -9.81: the scale reads {MASS_KG * (G - G):.1f} N")
