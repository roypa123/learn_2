# follow.py - a robot follows a walking person and tries to stay 1.0 m behind
wanted_gap = 1.0       # setpoint: 1.0 m behind the person
person_speed = 1.0     # the person walks at 1.0 m/s
dt = 0.1               # 10 loops per second

for gain in [2, 5]:
    person = 1.0       # the person starts 1.0 m ahead of the robot
    robot = 0.0
    for step in range(101):                    # 10 seconds
        gap = person - robot                   # SENSE: distance to the person
        error = gap - wanted_gap               # THINK: too far behind (+) or too close (-)?
        speed = gain * error                   #        drive faster when the error is bigger
        speed = max(0.0, min(2.0, speed))      #        the robot can only drive 0 to 2 m/s forward
        robot = robot + speed * dt             # ACT: drive for one loop
        person = person + person_speed * dt    # the person keeps walking
    print("gain", gain, "| after 10 s: gap", round(gap, 3), "m | error", round(error, 3), "m | robot speed", round(speed, 2), "m/s")
