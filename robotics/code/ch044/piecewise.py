# piecewise.py - functions made of pieces, and functions joined one after another
def saturate(x, limit):
    if x > limit:
        return limit
    if x < -limit:
        return -limit
    return x


def deadband(x, width):
    if abs(x) < width:
        return 0
    return x


def speed_command(stick):
    return saturate(deadband(stick, 5), 80)


print(" stick  deadband  saturate  both")
for stick in [-120, -60, -3, 0, 2, 7, 50, 95, 130]:
    print(f"{stick:6d} {deadband(stick, 5):9d} {saturate(stick, 80):9d} {speed_command(stick):5d}")
