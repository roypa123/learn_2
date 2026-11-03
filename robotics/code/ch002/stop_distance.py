# stop_distance.py - how far ahead must a warehouse robot see?
wait_time = 0.1        # worst case: the obstacle appears just after a sensor reading (10 readings per second)
think_time = 0.05      # the computer needs 0.05 s to decide
sensor_range = 2.0     # the sensor sees obstacles up to 2.0 m away

speeds = [1.0, 1.5, 2.0]            # metres per second
brake_distances = [0.50, 1.13, 2.00]  # metres, measured by the robot's maker

for i in range(3):
    speed = speeds[i]
    reaction = speed * (wait_time + think_time)   # distance driven before the brakes start
    total = reaction + brake_distances[i]         # distance driven until the robot stands still
    if total < sensor_range:
        result = "safe"
    else:
        result = "NOT safe"
    print("speed", speed, "m/s | reaction", round(reaction, 3), "m | total", round(total, 3), "m |", result)
