# cold_joint.py - what one bad solder joint does to Rover's motor supply
V_BATT = 7.2
R_INTERNAL = 0.146            # Rover's battery (Chapter 81)
R_MOTOR = 4.8                 # one motor, stalled at the start (Chapter 75)
R_DRIVER = 0.5                # the motor driver's switch (Chapter 88)
R_WIRES = 0.03                # good wires and connectors

for name, r_joint in [("good joint", 0.001), ("dull, grainy joint", 0.1), ("cracked cold joint", 1.0),
                      ("cracked, vibrating", 5.0)]:
    r_total = R_INTERNAL + R_DRIVER + R_WIRES + r_joint + R_MOTOR
    i = V_BATT / r_total                                  # Ohm's law for the whole loop (Chapter 75)
    p_joint = i ** 2 * r_joint                            # heat in the joint itself (Chapter 76)
    v_motor = i * R_MOTOR
    print(f"{name:20s} {r_joint:6.3f} ohm: motor gets {v_motor:4.2f} V, {i:4.2f} A; joint heat {p_joint * 1000:6.1f} mW")
