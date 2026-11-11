# drone_energy.py - how many joules, and how many coulombs, does a survey flight cost?
CELLS = 4
CELL_NOMINAL = 3.7            # volts per lithium cell, typical
CELL_FULL = 4.2
CELL_EMPTY = 3.3              # stop here (Chapter 89)
CAPACITY_MAH = 5000
USABLE = 0.80
MASS = 1.6
G = 9.81

v_nom = CELLS * CELL_NOMINAL
print(f"a {CELLS}S pack: {v_nom:.1f} V nominal, {CELLS * CELL_FULL:.1f} V full, {CELLS * CELL_EMPTY:.1f} V empty")
charge_c = CAPACITY_MAH / 1000 * 3600 * USABLE
energy_j = v_nom * charge_c
print(f"usable charge {charge_c:.0f} C, usable energy {energy_j:.0f} J = {energy_j / 3600:.1f} Wh")
print()

# the flight plan: climb, survey, descend. Energy per part, from Chapter 67's ideas
climb_j = MASS * G * 60 / 0.5              # lift 60 m, half the electrical energy ends up as height
survey_j = 180.0 * 8 * 60                  # 8 minutes at 180 W (hover-like flying)
descend_j = 120.0 * 60                     # 1 minute descending at 120 W
parts = [("climb to 60 m", climb_j), ("8 min survey", survey_j), ("descend", descend_j)]
total = 0.0
for name, joules in parts:
    coulombs = joules / v_nom
    total += joules
    print(f"{name:14s} {joules:8.0f} J = {coulombs:7.0f} C = {coulombs / 3.6:6.0f} mAh")
print(f"{'total':14s} {total:8.0f} J = {total / v_nom:7.0f} C = {total / v_nom / 3.6:6.0f} mAh")
print(f"that is {total / energy_j:.0%} of the usable energy")
