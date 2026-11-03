# prop_tip.py - how fast does the tip of a propeller move?
pi = 3.14159

names = ["toy drone", "racing drone", "camera drone", "farm drone"]
diameters = [0.04, 0.127, 0.24, 0.76]     # metres (0.127 m = 5 inches)
rpms = [30000, 30000, 7000, 3000]         # turns per minute at full power

for i in range(4):
    circumference = pi * diameters[i]           # metres the tip travels in one turn
    turns_per_second = rpms[i] / 60
    tip_speed = circumference * turns_per_second
    print(names[i], "| diameter", diameters[i], "m |", rpms[i], "rpm |", round(turns_per_second, 1),
          "turns/s | tip speed", round(tip_speed, 1), "m/s =", round(tip_speed * 3.6), "km/h")
