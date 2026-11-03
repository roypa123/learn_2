# design_check.py - does our tiny cleaning robot meet every requirement?
# --- power budget (Chapter 5) ---
watts = [0.25, 0.30, 2.00, 1.50, 0.20, 0.10]   # brain, motor driver, 2 drive motors, brush motor, 4 cliff sensors, encoders
battery_wh = 4.8 * 2.0                          # 4 x AA NiMH: 4.8 V, 2.0 Ah -> Wh = V x Ah
usable_wh = 0.8 * battery_wh                    # use only 80% (Chapter 5)
total_w = sum(watts)
battery_min = usable_wh / total_w * 60          # time = energy / power, in minutes

# --- stopping at a cliff (Chapter 2) ---
speed = 0.2           # m/s
loop_time = 0.02      # 50 loops per second
brake = 0.02          # metres to stop from 0.2 m/s (measured on a test floor)
stop_dist = speed * loop_time + brake
sensor_ahead = 0.04   # the cliff sensors look 4 cm in front of the wheels

# --- the requirements: name, design value, limit, "max" (must be <= limit) or "min" (must be >= limit) ---
names  = ["height (cm)", "width (cm)", "mass (kg)", "battery time (min)", "floor cleaned in 30 min (%)",
          "cost (dollars)", "cliff stopping distance (m)"]
values = [8.0, 20.0, 0.6, battery_min, 93.8, 96, stop_dist]
limits = [9.0, 25.0, 1.5, 45, 90, 100, sensor_ahead]
kinds  = ["max", "max", "max", "min", "min", "max", "max"]

print("total power", round(total_w, 2), "W | usable energy", usable_wh, "Wh")
all_ok = True
for i in range(len(names)):
    if kinds[i] == "max":
        ok = values[i] <= limits[i]
    else:
        ok = values[i] >= limits[i]
    if not ok:
        all_ok = False
    print(names[i], "| design", round(values[i], 3), "| limit", kinds[i], limits[i], "|", "PASS" if ok else "FAIL")
print("ALL REQUIREMENTS MET" if all_ok else "SOME REQUIREMENTS FAILED: change the design")
