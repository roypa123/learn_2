# power_budget.py - how long does Rover's battery last?
battery_wh = 7.2 * 2.0     # 6 rechargeable AA cells: 7.2 volts x 2.0 amp-hours = 14.4 Wh
usable = 0.8               # we only use 80% of the battery, to protect it

parts = ["Arduino board", "motor driver", "2 drive motors", "line sensor", "distance sensor"]
watts = [0.25, 0.3, 3.0, 0.15, 0.08]     # typical power of each part while Rover drives

total = 0
for i in range(len(parts)):
    print(parts[i], ":", watts[i], "W")
    total = total + watts[i]

hours = battery_wh * usable / total
print("total power:", round(total, 2), "W")
print("battery:", battery_wh, "Wh, usable:", round(battery_wh * usable, 2), "Wh")
print("driving time:", round(hours, 2), "hours =", round(hours * 60), "minutes")
