# tortoise.py - a light-seeking robot, in the spirit of the first electronic "tortoises" (1948-49)
import math

light_x, light_y = 0.0, 0.0      # the lamp is at (0, 0)
x, y = -3.0, -2.0                # the robot starts here (metres)
heading = 0.0                    # direction it faces, in degrees (0 = east, 90 = north)
speed = 0.1                      # metres per step
turn_gain = 400                  # how strongly it turns towards the brighter side


def brightness(px, py):
    # light gets weaker with distance: 1 at the lamp, smaller far away
    d2 = (px - light_x) ** 2 + (py - light_y) ** 2
    return 1 / (1 + d2)


for step in range(100):
    # SENSE: two light sensors, 0.2 m in front, 30 degrees to the left and to the right
    left_angle = math.radians(heading + 30)
    right_angle = math.radians(heading - 30)
    left = brightness(x + 0.2 * math.cos(left_angle), y + 0.2 * math.sin(left_angle))
    right = brightness(x + 0.2 * math.cos(right_angle), y + 0.2 * math.sin(right_angle))

    # THINK: turn towards the brighter side; stop when the light is very bright
    if brightness(x, y) > 0.9:
        print("step", step, "| reached the light at", round(x, 2), round(y, 2))
        break
    turn = turn_gain * (left - right)

    # ACT: turn, then drive one step forward
    heading = heading + turn
    x = x + speed * math.cos(math.radians(heading))
    y = y + speed * math.sin(math.radians(heading))
    if step % 10 == 0:
        print("step", step, "| left", round(left, 3), "| right", round(right, 3),
              "| turn", round(turn, 1), "| position", round(x, 2), round(y, 2))
