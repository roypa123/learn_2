# coulomb_count.py - two ways for a drone to know how much battery is left during a flight
from lipo_model import ocv, soc_from_ocv

CAPACITY_MAH = 5000.0
CELLS = 4
R_PACK = 0.020
DT = 0.1                                   # the flight controller measures 10 times a second

# a flight plan: (seconds, current in A)
plan = [(10, 60), (120, 25), (20, 90), (180, 28), (30, 120)]

soc, used_mah, t = 1.0, 0.0, 0.0
print(f"{'time':>6s} {'current':>8s} {'true charge':>12s} {'coulomb count':>14s} {'from voltage':>13s}")
for seconds, amps in plan:
    for _ in range(int(seconds / DT)):
        used_mah += amps * DT / 3.6        # A x s = coulombs; / 3.6 = mAh (Chapter 74)
        soc -= amps * DT / 3600 / (CAPACITY_MAH / 1000)
        t += DT
    v_pack = CELLS * ocv(soc) - amps * R_PACK
    guess_v = soc_from_ocv(v_pack / CELLS)          # naive: read the loaded voltage as if it were resting
    count = 1 - used_mah / CAPACITY_MAH
    print(f"{t:5.0f}s {amps:6d} A {soc:11.1%} {count:13.1%} {guess_v:12.1%}")
print(f"used {used_mah:.0f} mAh of {CAPACITY_MAH:.0f}; the 80% rule allows {0.8 * CAPACITY_MAH:.0f} mAh: time to land")
