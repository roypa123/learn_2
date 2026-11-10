# gear_train.py - exact speed and torque through a chain of gears
from fractions import Fraction

stages = [(12, 60), (15, 45), (10, 40)]    # (driving teeth, driven teeth)
motor_rpm = 6000
motor_torque_nm = 0.05
efficiency_per_stage = 0.95

speed_ratio = Fraction(1, 1)
for driving, driven in stages:
    stage = Fraction(driving, driven)
    speed_ratio = speed_ratio * stage
    print(f"{driving:>3} drives {driven:<3} stage {str(stage):<5} total {speed_ratio}")

efficiency = efficiency_per_stage ** len(stages)
output_rpm = motor_rpm * speed_ratio
output_torque = motor_torque_nm / speed_ratio * efficiency

print(f"output speed : {float(output_rpm):.1f} rpm")
print(f"efficiency   : {efficiency:.1%}")
print(f"output torque: {float(output_torque):.2f} N m")
