# watchdog.py - what does a robot do when its remote control goes silent?
speed_command = 0.5    # the remote control says: drive forward at 0.5 m/s
link_lost_step = 20    # at loop 20 (2.0 s) the radio link breaks
max_silent = 3         # the watchdog stops the robot after 3 loops without a message
dt = 0.1               # one loop every 0.1 s (10 loops per second)

for use_watchdog in [False, True]:
    position = 0.0
    speed = 0.0
    silent = 0                                  # how many loops since the last message
    for step in range(51):                      # 5 seconds
        if step < link_lost_step:               # SENSE: did a message arrive in this loop?
            speed = speed_command
            silent = 0
        else:
            silent = silent + 1
        if use_watchdog and silent >= max_silent and speed > 0:   # THINK: silent for too long?
            speed = 0.0
            print("  t =", round(step * dt, 1), "s: no message for", silent, "loops -> STOP")
        position = position + speed * dt        # ACT: drive for one loop
    print("watchdog", use_watchdog, "| final position", round(position, 2), "m | driven after the link broke",
          round(position - speed_command * link_lost_step * dt, 2), "m")
