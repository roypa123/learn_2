# drone_charge.py - a drone battery as a tank of charge: how long does the charge last?
ELECTRON_C = 1.602e-19

CAPACITY_MAH = 5000
USABLE = 0.80                       # never empty a LiPo completely (Chapter 89)
HOVER_A = 25.0                      # current while hovering
FAST_A = 40.0                       # current while flying fast

full_c = CAPACITY_MAH / 1000 * 3600
usable_c = full_c * USABLE
print(f"battery: {CAPACITY_MAH} mAh = {full_c:.0f} C, usable {usable_c:.0f} C")
print(f"that is {usable_c / ELECTRON_C:.2e} electrons we may use")
print()

for name, amps in [("hover", HOVER_A), ("fast flight", FAST_A)]:
    seconds = usable_c / amps                     # charge left / charge per second
    print(f"{name:12s} {amps:5.1f} A: {amps / ELECTRON_C:.2e} electrons per second, lasts {seconds:5.0f} s = {seconds / 60:4.1f} min")

print()
# a mission: 2 min climb at 35 A, then hover for the rest
climb_c = 35.0 * 120
left = usable_c - climb_c
print(f"a 2 min climb at 35 A uses {climb_c:.0f} C, leaving {left:.0f} C")
print(f"hover time after the climb: {left / HOVER_A / 60:.1f} min")
