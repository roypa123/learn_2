# motor_command.py - turn a signed speed percentage into what the motor driver needs
MAX_PWM = 255


def motor_command(percent):
    if percent > 100:
        percent = 100
    if percent < -100:
        percent = -100
    if percent >= 0:
        direction = "forward"
    else:
        direction = "backward"
    pwm = round(abs(percent) / 100 * MAX_PWM)
    return direction, pwm


for speed in [0, 25, 50, 100, -25, -100, 140, -300]:
    direction, pwm = motor_command(speed)
    print(f"{speed:5d}%  {direction:<9} pwm {pwm:3d}")
