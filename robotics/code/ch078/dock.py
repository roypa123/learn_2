# dock.py - Rover on its charging dock: the charger, the battery and the robot all meet at one node
from nodal import solve

CHARGER_V, CHARGER_OHM = 8.4, 0.5         # the dock's supply and its resistance (wires, contacts)
BATTERY_V, BATTERY_OHM = 7.2, 0.15        # Rover's battery: its voltage now, and inside resistance
ROBOT_OHM = 13.6                          # Rover's electronics and idling motors: 7.2 V / 0.53 A

# node 1 is the robot's power rail; every part joins it to ground
v = solve(1, [(1, 0, ROBOT_OHM)], [(1, 0, CHARGER_V, CHARGER_OHM), (1, 0, BATTERY_V, BATTERY_OHM)])
rail = v[1]
i_charger = (CHARGER_V - rail) / CHARGER_OHM      # out of the charger into the rail
i_battery = (BATTERY_V - rail) / BATTERY_OHM      # out of the battery (negative = charging)
i_robot = rail / ROBOT_OHM
print(f"rail voltage {rail:.3f} V")
print(f"charger gives {i_charger:+.3f} A, battery gives {i_battery:+.3f} A, robot takes {i_robot:.3f} A")
print(f"current law check: {i_charger:.3f} + ({i_battery:.3f}) = {i_charger + i_battery:.3f} A = robot {i_robot:.3f} A")
print()

print("as the battery fills, its voltage rises and the charging current falls:")
for bv in [6.6, 7.0, 7.2, 7.6, 8.0, 8.2, 8.4]:
    rail = solve(1, [(1, 0, ROBOT_OHM)], [(1, 0, CHARGER_V, CHARGER_OHM), (1, 0, bv, BATTERY_OHM)])[1]
    into_battery = (rail - bv) / BATTERY_OHM
    print(f"  battery at {bv:.1f} V: rail {rail:.3f} V, charging current {into_battery:+.3f} A")
