# gearbox.py - a gear pair divides speed and multiplies torque; the power stays (almost) the same
import math

MOTOR_RPM = 6000
MOTOR_TORQUE_NM = 0.05
STAGE_EFFICIENCY = 0.95

stages = [(12, 60), (15, 45), (10, 40)]     # (teeth on the driving gear, teeth on the driven gear)

rpm, torque = MOTOR_RPM, MOTOR_TORQUE_NM
print("stage   ratio   speed (rpm)   torque (N m)   power (W)")
print(f"motor           {rpm:9.1f}   {torque:10.4f}   {torque * rpm * 2 * math.pi / 60:8.2f}")
for k, (driving, driven) in enumerate(stages, start=1):
    ratio = driven / driving
    rpm = rpm / ratio
    torque = torque * ratio * STAGE_EFFICIENCY
    power = torque * rpm * 2 * math.pi / 60          # P = torque x omega
    print(f"{k:5d}   {ratio:5.1f}   {rpm:11.1f}   {torque:12.4f}   {power:9.2f}")

total = 1
for driving, driven in stages:
    total = total * driven / driving
print(f"total ratio {total:.0f}:1, efficiency {STAGE_EFFICIENCY ** len(stages):.1%}")
