# robot_trip.py - the trip from Figure 1.3
speed_a = 0.2      # part A: speed in metres per second
time_a = 5         # part A: time in seconds
time_b = 3         # part B: the robot is stopped, time in seconds
speed_c = 0.4      # part C: speed in metres per second
time_c = 3         # part C: time in seconds

distance_a = speed_a * time_a
distance_c = speed_c * time_c
total_distance = distance_a + distance_c
total_time = time_a + time_b + time_c
average_speed = total_distance / total_time

print("Distance in part A:", distance_a, "m")
print("Distance in part C:", round(distance_c, 2), "m")
print("Total distance:", round(total_distance, 2), "m")
print("Total time:", total_time, "s")
print("Average speed:", round(average_speed, 3), "m/s")
