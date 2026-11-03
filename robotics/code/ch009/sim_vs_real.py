# sim_vs_real.py - Rover stops at a wall: a perfect simulation and a more "real" one
import random
random.seed(1)            # the same "random" numbers every run, so results can be compared

setpoint = 0.3            # stop 0.3 m from the wall
gain = 2.0                # speed command = gain x error
max_speed = 0.25          # m/s
dt = 0.1                  # 10 loops per second

for world in ["perfect", "real"]:
    distance = 1.0
    for step in range(61):                                  # 6 seconds
        measured = distance                                 # SENSE
        if world == "real":
            measured = distance + random.uniform(-0.01, 0.01)   # the sensor is noisy: +/- 1 cm
        command = gain * (measured - setpoint)              # THINK
        command = max(0.0, min(max_speed, command))
        speed = command                                     # ACT
        if world == "real":
            speed = 0.85 * command                          # the motors are a bit weaker than promised
            if command < 0.05:
                speed = 0.0                                 # friction: too little power, the wheels do not turn
        distance = distance - speed * dt
    print(world, "world | final distance", round(distance, 3), "m | error", round(distance - setpoint, 3), "m")
