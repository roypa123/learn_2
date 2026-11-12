# moth_sim.py - Moth drives on the floor: two eyes, two transistor channels, two wheels, and a lamp
import math
from moth_channel import channel, I_START, I_MAX

LAMP_LUX_AT_1M = 400.0        # a bright desk lamp on the floor: 400 lux at 1 m, falling as 1 / distance squared
AMBIENT = 15.0                # a dim room
EYE_ANGLE = math.radians(35)  # each eye looks 35 degrees to its side
V_MAX = 0.20                  # wheel speed at full motor current, m/s
TRACK = 0.10                  # distance between the wheels, m
DT = 0.01


def eye_lux(x, y, heading, side, lamp):
    """Light reaching one eye: room light, plus the lamp if the eye is facing it."""
    dx, dy = lamp[0] - x, lamp[1] - y
    d = max(math.hypot(dx, dy), 0.05)
    eye_dir = heading + side * EYE_ANGLE                  # side: +1 left eye, -1 right eye
    facing = math.cos(math.atan2(dy, dx) - eye_dir)        # 1 when the eye looks straight at the lamp
    return AMBIENT + LAMP_LUX_AT_1M / d ** 2 * max(0.0, facing)


def wheel_speed(lux):
    i_c = channel(lux)[1]
    return V_MAX * min(max((i_c - I_START) / (I_MAX - I_START), 0.0), 1.0)


def simulate(crossed, lamp, x=0.0, y=0.0, heading=0.0, seconds=60.0, bias=0.0):
    path = [(x, y)]
    t = 0.0
    while t < seconds:
        left, right = eye_lux(x, y, heading, +1, lamp) + bias, eye_lux(x, y, heading, -1, lamp)
        if crossed:
            v_left, v_right = wheel_speed(right), wheel_speed(left)    # each eye drives the OPPOSITE wheel
        else:
            v_left, v_right = wheel_speed(left), wheel_speed(right)    # each eye drives its own side's wheel
        v = (v_left + v_right) / 2                                     # forward speed
        w = (v_right - v_left) / TRACK                                 # turning speed, rad/s (left is positive)
        x += v * math.cos(heading) * DT
        y += v * math.sin(heading) * DT
        heading += w * DT
        t += DT
        path.append((x, y))
        if math.hypot(lamp[0] - x, lamp[1] - y) < 0.12:
            return path, f"reached the lamp after {t:.1f} s"
        if v_left < 0.001 and v_right < 0.001:                          # under 1 mm/s: stopped
            return path, f"stopped after {t:.1f} s, {math.hypot(lamp[0] - x, lamp[1] - y):.2f} m from the lamp (too dark)"
    return path, f"still driving after {seconds:.0f} s"


if __name__ == "__main__":
    LAMP = (1.5, 1.0)
    for label, crossed, heading in [("crossed wires (Moth), lamp ahead-left", True, 0.0),
                                    ("straight wires, lamp ahead-left", False, 0.0),
                                    ("crossed wires, lamp behind", True, math.pi)]:
        path, result = simulate(crossed, LAMP, heading=heading)
        print(f"{label:40s} {result}")
