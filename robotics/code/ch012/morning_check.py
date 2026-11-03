# morning_check.py - the robot arm's daily checks, always the same, always in order
pressure_bar = 6.1
backup_v = 25.4
temperature_c = 38
print("air pressure OK:", pressure_bar >= 5.5)
print("backup battery OK:", backup_v >= 24.0)
print("temperature OK:", temperature_c <= 45)
