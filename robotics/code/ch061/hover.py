# hover.py - how much thrust does a drone need to hover, climb and descend?
G = 9.81
MASS_KG = 1.2            # the whole drone with its battery
MOTORS = 4
MAX_THRUST_PER_MOTOR_N = 6.0

weight = MASS_KG * G
print(f"weight {weight:.2f} N, so hover needs {weight:.2f} N in total, {weight / MOTORS:.2f} N per motor")

for a in [0.0, 2.0, 5.0, -2.0]:
    thrust = MASS_KG * (G + a)              # net upward force = thrust - weight = m a
    share = thrust / (MOTORS * MAX_THRUST_PER_MOTOR_N)
    print(f"vertical acceleration {a:+4.1f} m/s^2 needs thrust {thrust:5.2f} N  ({share:.0%} of maximum)")

max_up = MOTORS * MAX_THRUST_PER_MOTOR_N / MASS_KG - G
print(f"thrust-to-weight ratio {MOTORS * MAX_THRUST_PER_MOTOR_N / weight:.2f}, fastest upward acceleration {max_up:.2f} m/s^2")
