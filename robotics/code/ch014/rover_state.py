# rover_state.py - Rover's STATE: a few variables that describe it right now
POWER_W = 3.78                # CONSTANT (capitals): Rover's power while driving (Chapter 5)
SPEED_MS = 0.25               # CONSTANT: Rover's cruising speed in metres per second
BATTERY_START_WH = 11.52      # CONSTANT: usable energy when full, 80% of 14.4 Wh (Chapter 5)

x_m, y_m = 0.0, 0.0           # STATE: position on the floor in metres (the start)
heading_deg = 90              # STATE: facing east (0 = north, 90 = east; Chapter 13)
battery_wh = BATTERY_START_WH # STATE: energy left
odometer_m = 0.0              # STATE: total distance driven so far
print("start: x", x_m, "y", y_m, "heading", heading_deg, "battery", battery_wh, "Wh")

leg_m = 2.0                   # leg 1: drive 2 m
x_m += leg_m                  # facing east, so only x changes
odometer_m += leg_m
battery_wh -= POWER_W * (leg_m / SPEED_MS) / 3600   # energy = power x time in hours
print("leg 1: x", x_m, "y", y_m, "heading", heading_deg, "battery", round(battery_wh, 4), "Wh")

heading_deg = (heading_deg - 90) % 360   # turn left 90 degrees: now facing north
leg_m = 1.5                   # leg 2: drive 1.5 m
y_m += leg_m                  # facing north, so only y changes
odometer_m += leg_m
battery_wh -= POWER_W * (leg_m / SPEED_MS) / 3600
print("leg 2: x", x_m, "y", y_m, "heading", heading_deg, "battery", round(battery_wh, 4), "Wh")

used_wh = BATTERY_START_WH - battery_wh
print("odometer:", odometer_m, "m | used:", round(used_wh, 4), "Wh =", round(used_wh / BATTERY_START_WH * 100, 2), "%")
