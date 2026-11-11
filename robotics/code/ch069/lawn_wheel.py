# lawn_wheel.py - choosing the wheel size for a robot lawn mower that drives on grass
import math

G = 9.81
MASS_KG = 12.0
SPEED = 0.5                    # m/s while mowing
EFFICIENCY = 0.7
C_RR_AT_10CM = 0.08            # rolling resistance on short grass with 10 cm wheels (measured)
BUMP_M = 0.03                  # the mower must roll over 3 cm bumps and roots

print(" wheel    C_rr    rolling force   power   wheel rpm   torque per wheel   bump / radius")
for d_cm in [10, 15, 20, 25, 30]:
    d = d_cm / 100
    c_rr = C_RR_AT_10CM * math.sqrt(0.10 / d)          # rough rule: C_rr falls with 1 / sqrt(diameter)
    force = c_rr * MASS_KG * G
    power = force * SPEED / EFFICIENCY
    rpm = SPEED / (d / 2) * 60 / (2 * math.pi)
    torque = force / 2 * (d / 2)                          # two driven wheels share the push
    print(f"{d_cm:3d} cm   {c_rr:5.3f}   {force:9.2f} N   {power:5.1f} W   {rpm:7.1f}   {torque:10.3f} N m   {BUMP_M / (d / 2):10.2f}")
