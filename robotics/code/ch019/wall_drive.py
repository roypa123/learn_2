# wall_drive.py - Rover drives up to a wall and stops: a real control loop in simulation
SETPOINT_M = 0.30                  # stop this far from the wall
GAIN = 1.0                         # speed command per metre of error (Chapter 18)
MAX_SPEED_MS = 0.25                # the clamp
DEADBAND_M = 0.01                  # close enough
DT_S = 0.5                         # time for one trip round the loop, in seconds
MAX_STEPS = 50                     # safety: never loop more than this

distance_m = 1.0                   # STATE: the wall starts 1 m away
time_s = 0.0                       # STATE: the clock
steps = 0                          # STATE: how many times we have gone round

error_m = distance_m - SETPOINT_M
while abs(error_m) >= DEADBAND_M and steps < MAX_STEPS:
    speed_ms = GAIN * error_m      # think
    if speed_ms > MAX_SPEED_MS:    # clamp
        speed_ms = MAX_SPEED_MS
    elif speed_ms < -MAX_SPEED_MS:
        speed_ms = -MAX_SPEED_MS

    distance_m -= speed_ms * DT_S  # act: driving forward makes the distance smaller
    time_s += DT_S
    steps += 1
    error_m = distance_m - SETPOINT_M   # sense again
    print(f"t={time_s:4.1f} s  speed {speed_ms:+.3f}  distance {distance_m:.3f} m")

print("stopped after", steps, "steps at", round(distance_m, 3), "m")
