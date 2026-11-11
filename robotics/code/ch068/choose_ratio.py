# choose_ratio.py - pick a gear ratio so a robot is fast enough on the flat AND strong enough on a ramp
import math

G = 9.81
MASS_KG = 4.0                 # Rover
WHEEL_R = 0.033               # m
FREE_RPM = 12000              # motor speed with no load
STALL_NM = 0.010              # motor torque when held still
EFFICIENCY = 0.80             # gearbox
DRIVEN_WHEELS = 2
NEED_SPEED = 0.6              # m/s on the flat
RAMP_PERCENT = 20             # must climb this ramp...
RAMP_SPEED = 0.2              # ...at this speed or more


def wheel_force_at(speed, ratio):
    """Total push from both wheels at a given robot speed: motor torque falls in a straight line with speed."""
    motor_rad_s = speed / WHEEL_R * ratio
    free_rad_s = FREE_RPM * 2 * math.pi / 60
    motor_torque = STALL_NM * max(0.0, 1 - motor_rad_s / free_rad_s)
    return DRIVEN_WHEELS * motor_torque * ratio * EFFICIENCY / WHEEL_R


ramp_force = MASS_KG * G * math.sin(math.atan(RAMP_PERCENT / 100)) + 0.015 * MASS_KG * G
flat_force = 0.015 * MASS_KG * G
print(f"push needed: {flat_force:.2f} N on the flat, {ramp_force:.2f} N on the {RAMP_PERCENT}% ramp")
print(" ratio   top speed (m/s)   push at 0.2 m/s   flat ok   ramp ok")
for ratio in [10, 20, 30, 50, 80, 120]:
    top = FREE_RPM * 2 * math.pi / 60 / ratio * WHEEL_R          # wheel speed when the motor spins freely
    flat_ok = wheel_force_at(NEED_SPEED, ratio) >= flat_force
    push = wheel_force_at(RAMP_SPEED, ratio)
    print(f"{ratio:5d}   {top:12.2f}   {push:13.2f} N   {str(flat_ok):>7}   {str(push >= ramp_force):>7}")
