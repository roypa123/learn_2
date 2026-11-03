# trip_time.py - how fast is the robot, and how long is its trip?
rpm = 120                    # wheel turns per minute
wheel_diameter = 0.2         # metres
route = 900                  # metres from the loading dock to shelf row K

circumference = 3.14159 * wheel_diameter
speed = rpm / 60 * circumference           # turns per second x metres per turn = m/s
total_s = round(route / speed)             # whole seconds for the trip
minutes = total_s // 60
seconds = total_s % 60

print("speed:", round(speed, 3), "m/s =", round(speed * 3.6, 2), "km/h")
print("trip:", total_s, "s =", minutes, "min", seconds, "s")
