# friction_basics.py - the friction limit F <= mu N, and finding mu by tilting a ramp
import math

G = 9.81
MASS_KG = 2.0
MU_STATIC = 0.5
MU_SLIDING = 0.4

normal = MASS_KG * G                       # on a flat floor the floor pushes up with the weight
limit = MU_STATIC * normal
print(f"normal force {normal:.2f} N, friction can hold up to {limit:.2f} N")
for push in [2.0, 6.0, 9.0, 10.0, 12.0]:
    if push <= limit:
        print(f"push {push:5.1f} N: stays still, friction pushes back {push:5.1f} N")
    else:
        sliding = MU_SLIDING * normal
        a = (push - sliding) / MASS_KG
        print(f"push {push:5.1f} N: slides, friction {sliding:.2f} N, a = {a:.2f} m/s^2")

print("tilt test: the block starts to slide when tan(angle) = mu")
for angle_deg in [15, 22, 26.6, 30]:
    t = math.tan(math.radians(angle_deg))
    print(f"  ramp at {angle_deg:4.1f} deg: tan = {t:.3f} -> {'slides' if t > MU_STATIC else 'stays'}")
print(f"a block that just starts to slide at 26.6 deg has mu = {math.tan(math.radians(26.6)):.2f}")
