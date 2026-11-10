# trip_ask.py - ask a person for a route and a speed, then show the trip time
route_m = float(input("How far is the route (m)? "))
speed_ms = float(input("How fast is the robot (m/s)? "))

total_s = round(route_m / speed_ms)
print("The trip takes", total_s // 60, "min", total_s % 60, "s")
