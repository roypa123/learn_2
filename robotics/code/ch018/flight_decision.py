# flight_decision.py - say GO or DO NOT FLY, and give every reason
CELLS = 4
MIN_CELL_V = 3.7
MIN_SATELLITES = 6
MAX_WIND_MS = 10.0

battery_v = float(input("Battery voltage (V): "))
satellites = int(input("Satellites: "))
wind_ms = float(input("Wind (m/s): "))
people_clear = input("Area clear of people? (y/n): ").strip().lower() == "y"

problems = 0                       # a counter (Chapter 14)

if battery_v / CELLS < MIN_CELL_V:
    print("- battery too low")
    problems += 1
if satellites < MIN_SATELLITES:
    print("- not enough satellites")
    problems += 1
if wind_ms > MAX_WIND_MS:
    print("- too windy")
    problems += 1
if not people_clear:
    print("- area not confirmed clear")
    problems += 1

if problems == 0:
    print("GO")
else:
    print("DO NOT FLY:", problems, "problem(s)")
