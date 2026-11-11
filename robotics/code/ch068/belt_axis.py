# belt_axis.py - a stepper motor moves a 3D printer's print head with a toothed belt
import math

STEPS_PER_REV = 200           # a common stepper motor: 1.8 degrees per step
MICROSTEPS = 16               # the driver splits each step into 16 (Chapter 145)
PULLEY_TEETH = 20             # GT2 pulley on the motor
BELT_PITCH_MM = 2.0           # GT2 belt: one tooth every 2 mm
MOTOR_TORQUE_NM = 0.40

mm_per_rev = PULLEY_TEETH * BELT_PITCH_MM
steps_per_mm = STEPS_PER_REV * MICROSTEPS / mm_per_rev
pulley_radius_m = mm_per_rev / (2 * math.pi) / 1000
belt_force = MOTOR_TORQUE_NM / pulley_radius_m

print(f"one motor turn moves the belt {mm_per_rev:.0f} mm")
print(f"{steps_per_mm:.0f} microsteps per mm, so one microstep is {1000 / steps_per_mm:.1f} micrometres")
print(f"pulley radius {pulley_radius_m * 1000:.2f} mm, so {MOTOR_TORQUE_NM} N m pulls the belt with {belt_force:.0f} N")

for speed_mm_s in [50, 150, 300]:
    rpm = speed_mm_s / mm_per_rev * 60
    print(f"print head at {speed_mm_s:3d} mm/s: motor at {rpm:5.0f} rpm, {speed_mm_s * steps_per_mm:6.0f} microsteps per second")
