# keyboard_rover.py - drive a simulated Rover with numbers typed on the keyboard
POWER_W = 3.78                     # Rover's power while driving (Chapter 5)
x_m = 0.0                          # STATE: position along the floor
battery_wh = 11.52                 # STATE: usable energy left

print("=== Rover console ===")
print("Type a speed (m/s) and a time (s), for example: 0.25 8")
print("A negative speed drives backwards.")
print()                            # an empty line

text = input("move 1> ")           # the program waits here for the person
speed_text, time_text = text.split()
speed_ms = float(speed_text)
time_s = float(time_text)
x_m += speed_ms * time_s
battery_wh -= POWER_W * time_s / 3600
print(f"   x = {x_m:.2f} m | battery {battery_wh:.4f} Wh")

text = input("move 2> ")           # the same steps again (a loop comes in Chapter 19)
speed_text, time_text = text.split()
speed_ms = float(speed_text)
time_s = float(time_text)
x_m += speed_ms * time_s
battery_wh -= POWER_W * time_s / 3600
print(f"   x = {x_m:.2f} m | battery {battery_wh:.4f} Wh")

print()
print("Rover stopped at", round(x_m, 2), "m")
