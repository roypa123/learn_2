# cliff_check.py - does a robot vacuum stop before the stairs?
speed = 0.3            # metres per second
look_ahead = 0.020     # the cliff sensor sees the edge 20 mm before the wheel reaches it
stop_needs = 0.010     # after the motors are told to stop, the robot still rolls 10 mm

for loops_per_second in [10, 25, 50, 100]:
    loop_time = 1 / loops_per_second              # seconds between two loops
    late = speed * loop_time                      # worst case: the edge appears just after a sense step
    needed = late + stop_needs                    # distance used before the robot is stopped
    if needed < look_ahead:
        result = "safe"
    else:
        result = "FALLS"
    print(loops_per_second, "loops/s | moves", round(late * 1000, 1), "mm per loop | needs",
          round(needed * 1000, 1), "mm |", result)
