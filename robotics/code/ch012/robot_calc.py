# robot_calc.py - three quick robot calculations from Part 1, saved so they can be run again
speed = 0.5                  # Rover's speed in m/s
loop_time = 0.02             # 50 loops per second
print("blind distance:", speed * loop_time, "m")

usable_wh = 0.8 * 14.4       # 80% of Rover's 14.4 Wh battery (Chapter 5)
power_w = 3.78               # Rover's total power in watts
print("battery time:", round(usable_wh / power_w * 60), "minutes")

tip_speed = 3.14159 * 0.127 * 30000 / 60    # racing-drone propeller (Chapter 7)
print("propeller tip speed:", round(tip_speed, 1), "m/s")
