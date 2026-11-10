# deliveries.py - a counter and a running total for a warehouse robot's shift
SPEED_MS = 1.257              # the robot's speed from Chapter 13 (120 rpm, 0.2 m wheels)
deliveries = 0                # a COUNTER: starts at 0 and goes up by 1
total_m = 0.0                 # a RUNNING TOTAL: starts at 0 and adds each trip

trip_m = 120.0                # delivery 1
deliveries += 1
total_m += trip_m

trip_m = 85.5                 # delivery 2: the same three lines again
deliveries += 1
total_m += trip_m

trip_m = 240.0                # delivery 3
deliveries += 1
total_m += trip_m

average_m = total_m / deliveries
drive_s = round(total_m / SPEED_MS)
print("deliveries:", deliveries, "| total:", total_m, "m | average:", average_m, "m")
print("driving time:", drive_s, "s =", drive_s // 60, "min", drive_s % 60, "s")
