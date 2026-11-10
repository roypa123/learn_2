# wall_controller.py - one step of Rover's wall-stopping controller
SETPOINT_M = 0.30                  # stop this far from the wall
GAIN = 1.0                         # speed command per metre of error (Chapter 6)
MAX_SPEED_MS = 0.25                # never command more than this
DEADBAND_M = 0.01                  # closer than this to the setpoint counts as "there"

distance_m = float(input("Distance to the wall (m): "))
error_m = distance_m - SETPOINT_M  # positive means we are too far away

if abs(error_m) < DEADBAND_M:      # close enough: do not fidget
    speed_ms = 0.0
else:
    speed_ms = GAIN * error_m      # proportional control

if speed_ms > MAX_SPEED_MS:        # clamp: not too fast forwards ...
    speed_ms = MAX_SPEED_MS
elif speed_ms < -MAX_SPEED_MS:     # ... and not too fast backwards
    speed_ms = -MAX_SPEED_MS

print(f"error {error_m:+.3f} m -> speed {speed_ms:+.3f} m/s")
