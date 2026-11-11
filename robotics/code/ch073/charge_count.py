# charge_count.py - how much charge is in a battery, and how many electrons that is
ELECTRON_C = 1.602e-19          # the charge of one electron, in coulombs (a minus sign in real life)
PER_COULOMB = 1 / ELECTRON_C    # electrons in one coulomb

print(f"one coulomb is {PER_COULOMB:.3e} electrons")
print()

batteries = [
    ("AA cell in Rover", 2000),
    ("phone", 4000),
    ("drone 4S LiPo", 5000),
    ("coin cell CR2032", 220),
]
print(f"{'battery':18s} {'mAh':>6s} {'coulombs':>10s} {'electrons':>12s}")
for name, mah in batteries:
    coulombs = mah / 1000 * 3600          # mAh -> Ah -> coulombs (1 A for 1 s = 1 C)
    electrons = coulombs * PER_COULOMB
    print(f"{name:18s} {mah:6d} {coulombs:10.0f} {electrons:12.3e}")

print()
current = 0.53                            # Rover's normal current, A (Chapter 7)
print(f"Rover at {current} A: {current:.2f} C every second = {current * PER_COULOMB:.2e} electrons per second")
print(f"a 2,000 mAh cell lasts {7200 / current / 3600:.2f} h at that current")
