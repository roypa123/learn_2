# shift_battery.py - how big a battery does a warehouse robot need for an 8-hour shift?
G = 9.81
MASS_KG = 60.0                 # the robot
LOAD_KG = 20.0                 # average load carried
SPEED = 1.5                    # m/s while driving
C_RR = 0.015                   # rolling resistance coefficient (Chapter 63)
DRIVE_EFFICIENCY = 0.70        # motor, gearbox and driver together
ELECTRONICS_W = 25.0           # computer, sensors, wifi: always on
SHIFT_H = 8.0
DRIVING_SHARE = 0.60           # it drives 60% of the time, waits the rest
STARTS_PER_HOUR = 120          # speeding up from rest to 1.5 m/s
LIFTS_PER_HOUR = 60            # lifting a 20 kg load by 0.5 m
LIFT_EFFICIENCY = 0.60

m = MASS_KG + LOAD_KG
rolling_w = C_RR * m * G * SPEED / DRIVE_EFFICIENCY
driving_wh = rolling_w * SHIFT_H * DRIVING_SHARE
starts_wh = STARTS_PER_HOUR * SHIFT_H * 0.5 * m * SPEED ** 2 / DRIVE_EFFICIENCY / 3600
lifts_wh = LIFTS_PER_HOUR * SHIFT_H * LOAD_KG * G * 0.5 / LIFT_EFFICIENCY / 3600
electronics_wh = ELECTRONICS_W * SHIFT_H
total_wh = driving_wh + starts_wh + lifts_wh + electronics_wh

print(f"rolling at {SPEED} m/s needs {rolling_w:.1f} W from the battery")
for name, wh in [("driving", driving_wh), ("speeding up", starts_wh), ("lifting", lifts_wh), ("electronics", electronics_wh)]:
    print(f"  {name:12s} {wh:7.1f} Wh  ({wh / total_wh:.0%})")
print(f"total for {SHIFT_H:.0f} hours: {total_wh:.0f} Wh")
print(f"battery with 25% spare and only 80% usable: {total_wh * 1.25 / 0.80:.0f} Wh")
