# safe_to_drive.py - decide if Rover may drive, using only True and False
MIN_WALL_M = 0.30                  # never drive closer to a wall than this
MIN_BATTERY_V = 6.0                # 6 cells x 1.0 V (Chapter 5)
CRUISE_MS = 0.25                   # normal speed in m/s

distance_m = 0.82                  # from the distance sensor
battery_v = 7.13                   # from the battery monitor
bumper_pressed = False             # is the bumper touching something?
e_stop_pressed = False             # has someone hit the emergency stop?

wall_clear = distance_m > MIN_WALL_M
battery_ok = battery_v >= MIN_BATTERY_V
bumper_clear = not bumper_pressed
e_stop_clear = not e_stop_pressed

safe_to_drive = wall_clear and battery_ok and bumper_clear and e_stop_clear
speed_ms = CRUISE_MS * safe_to_drive    # True counts as 1, False as 0

print("wall clear:   ", wall_clear)
print("battery ok:   ", battery_ok)
print("bumper clear: ", bumper_clear)
print("e-stop clear: ", e_stop_clear)
print("SAFE TO DRIVE:", safe_to_drive)
print("speed command:", speed_ms, "m/s")
