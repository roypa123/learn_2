# sensor_log.py - turn Arduino sensor lines into numbers and a tidy log
CELLS = 6                               # Rover's battery has 6 cells (Chapter 5)

line = "t=12.40;d=0.42;v=7.13\n"        # first line from the Arduino
t_part, d_part, v_part = line.strip().split(";")
time_s = float(t_part[2:])              # skip the first two characters: "t="
distance_m = float(d_part[2:])
battery_v = float(v_part[2:])
print(f"[{time_s:8.2f} s] dist {distance_m:6.3f} m | batt {battery_v:5.2f} V | cell {battery_v / CELLS:.3f} V")

line = "t=105.02;d=1.875;v=6.98\n"      # a later line: the same steps again
t_part, d_part, v_part = line.strip().split(";")
time_s = float(t_part[2:])
distance_m = float(d_part[2:])
battery_v = float(v_part[2:])
print(f"[{time_s:8.2f} s] dist {distance_m:6.3f} m | batt {battery_v:5.2f} V | cell {battery_v / CELLS:.3f} V")
