# centre_of_mass.py - where is Rover's centre of mass, front to back?
# Positions are in centimetres along the robot: 0 = the wheel axle, + = towards the front, - = towards the back.
# The caster (small free wheel) is at -9 cm. Rover is stable if the centre of mass is between -9 and 0 ... and
# safest when it is well inside that range.

names = ["chassis", "2 motors + wheels", "Arduino + driver", "sensors (front)", "battery"]
masses = [150, 160, 35, 30, 165]            # grams
positions_a = [-3, 0, -4, 7, 5]             # design A: battery in the FRONT (+5 cm)
positions_b = [-3, 0, -4, 7, -5]            # design B: battery in the BACK (-5 cm)

for design, positions in [["A (battery front)", positions_a], ["B (battery back)", positions_b]]:
    total_mass = 0
    total_moment = 0
    for i in range(len(names)):
        total_mass = total_mass + masses[i]
        total_moment = total_moment + masses[i] * positions[i]
    com = total_moment / total_mass
    print("design", design, "| mass", total_mass, "g | centre of mass at", round(com, 2), "cm")
