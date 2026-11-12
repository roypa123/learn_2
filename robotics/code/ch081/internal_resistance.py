# internal_resistance.py - measure a battery's internal resistance with a meter and two load resistors
# (example measurements of Rover's 6 x AA NiMH pack; replace them with your own)
readings = [
    # load resistor in ohms (None = no load), measured voltage at the terminals
    (None, 7.62),
    (22.0, 7.57),
    (10.0, 7.51),
    (4.7, 7.39),
]
v_open = readings[0][1]
print(f"open-circuit voltage: {v_open:.2f} V")
estimates = []
for r_load, v in readings[1:]:
    i = v / r_load                       # Ohm's law for the load resistor
    r_in = (v_open - v) / i              # the missing volts were lost inside the battery
    estimates.append(r_in)
    print(f"  {r_load:5.1f} ohm load: {v:.2f} V, current {i:.3f} A -> internal resistance {r_in:.3f} ohm")
avg = sum(estimates) / len(estimates)
print(f"average: {avg:.3f} ohm")
print(f"so a dead short would draw about {v_open / avg:.0f} A, and Rover's 3.1 A start sags the pack by {3.1 * avg:.2f} V")
