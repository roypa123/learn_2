# motor_guard.py - whatever goes wrong, the motors must end up off
def set_motors(speed):
    print(f"  motors at {speed:.2f} m/s")


def read_distance(step):
    """A pretend sensor that fails on the third reading."""
    if step == 2:
        raise OSError("sensor not responding")
    return 1.0 - step * 0.2


try:
    for step in range(5):
        distance_m = read_distance(step)
        set_motors(0.25)
        print("  distance", round(distance_m, 2))
except OSError as error:
    print("FAULT:", error)
finally:
    set_motors(0.0)               # this line runs however the block above ended
    print("motors are off")
