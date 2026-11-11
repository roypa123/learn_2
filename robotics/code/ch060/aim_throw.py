# aim_throw.py - find the throwing angles that land a parcel in the middle of the bin
from projectile import throw

SPEED = 4.665           # m/s, the launcher's fixed speed
START_HEIGHT = 0.5      # m
BIN_TOP = 0.3           # m
BIN_MIDDLE = 2.0        # m across

answers = []
previous = None
for k in range(1000, 8901):                  # angles 10.00 to 89.00 deg, in steps of 0.01 deg
    angle = k / 100
    result = throw(SPEED, angle, START_HEIGHT, BIN_TOP)
    miss = result[1] - BIN_MIDDLE            # + means too far, - means too short
    if previous is not None and (miss > 0) != (previous > 0):
        answers.append((angle, result))
    previous = miss

for angle, (t, x, top) in answers:
    print(f"aim at {angle:5.2f} deg: in the air {t:.3f} s, lands at {x:.3f} m, highest point {top:.2f} m")
