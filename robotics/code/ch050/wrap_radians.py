# wrap_radians.py - three ways to wrap an angle into -pi..pi, and how to unwrap a list
import math


def wrap_pi(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


def wrap_pi_trig(a):
    return math.atan2(math.sin(a), math.cos(a))


def unwrap(angles):
    result = [angles[0]]
    for a in angles[1:]:
        step = wrap_pi(a - result[-1])
        result.append(result[-1] + step)
    return result


for a in [3.0, 4.0, -4.0, 7.0, 100.0]:
    print(f"{a:6.1f} rad -> {wrap_pi(a):7.4f}  {wrap_pi_trig(a):7.4f}  {math.remainder(a, 2 * math.pi):7.4f}")

readings = [2.8, 3.0, -3.1, -2.9, -2.7, 3.1, 2.9]
print("raw     :", readings)
print("unwrapped:", [round(v, 2) for v in unwrap(readings)])
