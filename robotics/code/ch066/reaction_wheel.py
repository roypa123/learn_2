# reaction_wheel.py - a satellite turns itself by spinning a wheel the other way
import math

SAT_I = 20.0             # kg m^2, a small satellite about its turning axis
WHEEL_I = 0.002          # kg m^2, the small reaction wheel
WHEEL_MAX_RPM = 6000
TURN_DEG = 90

wheel_max = WHEEL_MAX_RPM * 2 * math.pi / 60
sat_max = WHEEL_I * wheel_max / SAT_I                # total angular momentum stays 0: I_s w_s = -I_w w_w
print(f"wheel at {WHEEL_MAX_RPM} rpm = {wheel_max:.1f} rad/s")
print(f"the satellite then turns the other way at {sat_max:.4f} rad/s = {math.degrees(sat_max):.2f} deg/s")

# spin the wheel up and down with a motor torque of 0.01 N m, to turn the satellite by 90 deg
TORQUE = 0.01
alpha_sat = TORQUE / SAT_I                           # the motor pushes the satellite back just as hard
angle = math.radians(TURN_DEG)
ramp = sat_max ** 2 / alpha_sat
if angle >= ramp:
    t = 2 * sat_max / alpha_sat + (angle - ramp) / sat_max
else:
    t = 2 * math.sqrt(angle / alpha_sat)
print(f"satellite alpha {alpha_sat:.4f} rad/s^2, a 90 deg turn takes {t:.1f} s")
print(f"angular momentum of the wheel at top speed: {WHEEL_I * wheel_max:.4f} kg m^2/s")
