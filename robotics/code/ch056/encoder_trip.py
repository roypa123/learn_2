# encoder_trip.py - a warehouse robot's odometer (distance) and where it is (displacement)
import math

TICKS_PER_REV = 1024
WHEEL_DIAMETER_M = 0.20
M_PER_TICK = math.pi * WHEEL_DIAMETER_M / TICKS_PER_REV

# signed tick counts read every second: + forwards along the aisle, - backwards
tick_log = [1630, 3260, 3260, 1630, 0, 0, -1630, -3260, -1630, 0, 1630, 1630]

position_m = 0.0
odometer_m = 0.0
for second, ticks in enumerate(tick_log, start=1):
    step_m = ticks * M_PER_TICK
    position_m = position_m + step_m
    odometer_m = odometer_m + abs(step_m)
    print(f"t = {second:2d} s   step {step_m:+6.3f} m   position {position_m:6.3f} m   odometer {odometer_m:6.3f} m")

print(f"metres per tick: {M_PER_TICK * 1000:.4f} mm")
print(f"displacement after {len(tick_log)} s: {position_m:+.2f} m")
print(f"distance on the odometer:   {odometer_m:.2f} m")
