# current_split.py - Rover's two motors in parallel on one battery: who gets how much current?
V_BATTERY = 7.2
R_INSIDE = 0.15                # the battery's internal resistance (in series with everything)
R_MOTOR = 4.8                  # each motor, stalled
WIRE_OHM_PER_M = 0.0336        # 0.5 mm2 copper
LEFT_WIRE_M = 0.3              # the left motor is near the battery
RIGHT_WIRE_M = 0.8             # the right motor's wire takes a longer route

# each branch = its motor plus its wire there and back (series)
r_left = R_MOTOR + 2 * LEFT_WIRE_M * WIRE_OHM_PER_M
r_right = R_MOTOR + 2 * RIGHT_WIRE_M * WIRE_OHM_PER_M
print(f"left branch  {r_left:.3f} ohm, right branch {r_right:.3f} ohm")

# the two branches are in parallel; that pair is in series with the battery's inside
r_pair = 1 / (1 / r_left + 1 / r_right)
i_total = V_BATTERY / (r_pair + R_INSIDE)
v_terminals = V_BATTERY - i_total * R_INSIDE
print(f"both together {r_pair:.3f} ohm; total current {i_total:.3f} A; battery terminals sag to {v_terminals:.3f} V")

# each branch has the terminal voltage across it
i_left, i_right = v_terminals / r_left, v_terminals / r_right
print(f"left motor {i_left:.3f} A, right motor {i_right:.3f} A (sum {i_left + i_right:.3f} A)")
print(f"the longer wire costs the right motor {(i_left - i_right) / i_left:.1%} of its current")

print()
# what if one motor is unplugged (its branch is open)?
i_one = V_BATTERY / (r_left + R_INSIDE)
print(f"with only the left motor: {i_one:.3f} A, terminals {V_BATTERY - i_one * R_INSIDE:.3f} V")
print("one branch open does not stop the other: that is the point of parallel wiring")
