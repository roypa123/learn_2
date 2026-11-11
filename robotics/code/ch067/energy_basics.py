# energy_basics.py - work, kinetic energy, potential energy and power for a delivery robot
G = 9.81
MASS_KG = 25.0

# work = force x distance (along the force)
print(f"pushing with 3.0 N for 100 m does {3.0 * 100:.0f} J of work")

# kinetic energy 1/2 m v^2: twice the speed, four times the energy
for v in [0.5, 1.0, 2.0]:
    ke = 0.5 * MASS_KG * v ** 2
    print(f"at {v:.1f} m/s the robot has {ke:6.1f} J of kinetic energy")

# braking: the brakes' work must remove all the kinetic energy
BRAKE_N = 37.5                            # 25 kg x 1.5 m/s^2
for v in [1.0, 2.0]:
    d = 0.5 * MASS_KG * v ** 2 / BRAKE_N
    print(f"from {v:.1f} m/s, a {BRAKE_N} N braking force stops it in {d:.3f} m")

# potential energy m g h: climbing 3 m (one floor) by a ramp
pe = MASS_KG * G * 3.0
print(f"climbing 3 m stores {pe:.1f} J = {pe / 3600:.3f} Wh")

# power = work / time = force x speed
for v in [0.5, 1.5]:
    print(f"pushing 3.0 N at {v} m/s needs {3.0 * v:.1f} W")
print(f"a 74 Wh battery holds {74 * 3600:,} J")
