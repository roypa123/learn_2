# hover_rpm.py - motor speed needed to hover, from thrust = K x rpm squared
import math

K = 4.08e-8        # newtons per (rpm squared), from a test: 8 N at 14000 rpm
GRAVITY = 9.81
MOTORS = 4
MAX_RPM = 14000

print("mass (kg)  thrust each (N)    rpm   % of max")
for mass_kg in [1.6, 1.92, 2.4, 3.2]:
    thrust_each = mass_kg * GRAVITY / MOTORS
    rpm = math.sqrt(thrust_each / K)
    print(f"{mass_kg:9.2f} {thrust_each:16.2f} {rpm:6.0f} {rpm / MAX_RPM:9.0%}")

max_total_thrust = MOTORS * K * MAX_RPM ** 2
print(f"maximum total thrust: {max_total_thrust:.1f} N")
print(f"heaviest it can hover: {max_total_thrust / GRAVITY:.2f} kg")
