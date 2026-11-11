# stopping_bisection.py - the fastest speed that still stops within 2 m, found by halving
REACTION_S = 0.3        # seconds before the brakes start
BRAKING = 1.5           # m/s squared
LIMIT_M = 2.0           # free space in front of the robot


def stopping_m(speed):
    return speed * REACTION_S + speed ** 2 / (2 * BRAKING)


def bisect(f, target, low, high, steps):
    for step in range(1, steps + 1):
        mid = (low + high) / 2
        if f(mid) < target:
            low = mid
        else:
            high = mid
        if step <= 6 or step == steps:
            print(f"step {step:2d}: speed between {low:.5f} and {high:.5f} m/s")
    return (low + high) / 2


best = bisect(stopping_m, LIMIT_M, 0.0, 5.0, 30)
print(f"fastest safe speed: {best:.4f} m/s")
print(f"check: stopping distance at that speed = {stopping_m(best):.6f} m")
