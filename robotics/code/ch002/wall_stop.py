# wall_stop.py - a robot drives towards a wall and stops (sense, think, act)
distance = 1.0        # metres from the wall at the start
speed = 0.25          # metres per second when driving
step_time = 0.5       # seconds between two loops
stop_distance = 0.3   # stop when the wall is this close (metres)

step = 0
moving = True
while moving:
    # SENSE: read the distance sensor
    reading = distance
    # THINK: decide what to do
    if reading > stop_distance:
        action = "forward"
    else:
        action = "stop"
    # ACT: move the robot, or stop it
    print("step", step, "| sensor:", round(reading, 3), "m | action:", action)
    if action == "forward":
        distance = distance - speed * step_time
    else:
        moving = False
    step = step + 1
