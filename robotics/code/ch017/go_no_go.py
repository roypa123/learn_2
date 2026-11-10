# go_no_go.py - a drone may fly only if EVERY check passes
CELLS = 4                          # a 4S battery (Chapter 16)
MIN_CELL_V = 3.7                   # do not take off below this
MIN_SATELLITES = 6                 # too few satellites means a poor position
MAX_WIND_MS = 10.0                 # too windy above this

battery_v = float(input("Battery voltage (V): "))
satellites = int(input("Satellites: "))
wind_ms = float(input("Wind (m/s): "))
people_clear = input("Area clear of people? (y/n): ").strip().lower() == "y"

battery_ok = battery_v / CELLS >= MIN_CELL_V
gps_ok = satellites >= MIN_SATELLITES
wind_ok = wind_ms <= MAX_WIND_MS

go = battery_ok and gps_ok and wind_ok and people_clear
failed = 4 - (battery_ok + gps_ok + wind_ok + people_clear)   # True counts as 1

print(f"battery {battery_ok} | gps {gps_ok} | wind {wind_ok} | people {people_clear}")
print(f"checks failed: {failed}")
print(f"GO: {go}")
