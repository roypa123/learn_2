# stopping_exact.py - the fastest safe speed for any free space, from the quadratic formula
from quadratic import solve_quadratic

REACTION_S = 0.3
BRAKING = 1.5


def safe_speed(free_m):
    a = 1 / (2 * BRAKING)
    b = REACTION_S
    c = -free_m
    roots = solve_quadratic(a, b, c)
    return max(roots)


print("free space (m)   fastest safe speed (m/s)")
for free in [0.5, 1.0, 2.0, 4.0, 8.0]:
    print(f"{free:14.1f} {safe_speed(free):18.4f}")
