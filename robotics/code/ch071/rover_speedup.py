# rover_speedup.py - Rover speeds up with a real motor whose torque falls with speed: no neat formula, so we step
import math

G = 9.81
MASS = 4.0
EFFECTIVE_MASS = MASS + 1.65          # plus the spinning motor rotors (Chapter 66)
WHEEL_R = 0.033
RATIO = 30
STALL_NM = 0.010
FREE_RAD_S = 12000 * 2 * math.pi / 60
EFFICIENCY = 0.80
ROLLING_N = 0.015 * MASS * G
DT = 0.001


def push(v):
    motor_speed = v / WHEEL_R * RATIO
    torque = STALL_NM * max(0.0, 1 - motor_speed / FREE_RAD_S)
    return 2 * torque * RATIO * EFFICIENCY / WHEEL_R


# top speed: the push falls in a straight line with speed, so solve push(v) = rolling resistance
push_at_rest = push(0.0)
v_free = FREE_RAD_S * WHEEL_R / RATIO                 # robot speed when the motors spin freely
v_top = v_free * (1 - ROLLING_N / push_at_rest)
print(f"top speed {v_top:.3f} m/s")

t, x, v = 0.0, 0.0, 0.0
marks = [0.25, 0.5, 0.75, 0.95]
while v < 0.95 * v_top:
    a = (push(v) - ROLLING_N) / EFFECTIVE_MASS
    x = x + v * DT
    v = v + a * DT
    t = t + DT
    if marks and v >= marks[0] * v_top:
        print(f"{marks[0]:.0%} of top speed ({v:.3f} m/s) after {t:.3f} s and {x:.3f} m")
        marks.pop(0)

a0 = (push(0) - ROLLING_N) / EFFECTIVE_MASS
print(f"starting acceleration {a0:.2f} m/s^2; at that rate it would reach 95% in {0.95 * v_top / a0:.3f} s")
