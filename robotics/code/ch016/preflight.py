# preflight.py - a drone checklist that waits for a person at every step
CELLS = 4                          # a "4S" battery: 4 cells in a row
CELL_EMPTY_V = 3.5                 # volts per cell when we call it empty
CELL_FULL_V = 4.2                  # volts per cell when full
FULL_FLIGHT_MIN = 15.0             # flight time with a full battery, in minutes

print("DRONE PRE-FLIGHT CHECK", "-" * 30, sep="\n")
pilot = input("Pilot name: ").strip()
input("1. Propellers tight, none cracked? Press Enter to confirm. ")
input("2. Nobody near the take-off area? Press Enter to confirm. ")
battery_v = float(input("3. Battery voltage (V): "))

cell_v = battery_v / CELLS
charge = (cell_v - CELL_EMPTY_V) / (CELL_FULL_V - CELL_EMPTY_V)   # 0 = empty, 1 = full
flight_min = FULL_FLIGHT_MIN * charge

print("-" * 30)
print(f"Pilot:        {pilot}")
print(f"Cell voltage: {cell_v:.2f} V")
print(f"Charge:       {charge:.0%}")
print(f"Flight time:  about {flight_min:.1f} min")
