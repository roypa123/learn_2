# wall_proportional.py - the robot from Chapter 2 again, but now it slows down near the wall
distance = 1.0        # metres from the wall at the start
step_time = 0.5       # seconds between two loops (as slow as in Chapter 2)
setpoint = 0.3        # we want to stop 0.3 m from the wall
gain = 1.0            # speed = gain x error
max_speed = 0.25      # the robot cannot drive faster than 0.25 m/s

for step in range(13):
    error = distance - setpoint                # SENSE + compare: how much further may we go?
    speed = gain * error                       # THINK: drive slower when the error is small
    speed = max(0.0, min(max_speed, speed))    #        but never faster than max_speed, never backwards
    print("step", step, "| distance", round(distance, 3), "m | error", round(error, 3), "m | speed", round(speed, 3), "m/s")
    distance = distance - speed * step_time    # ACT: drive for one loop
