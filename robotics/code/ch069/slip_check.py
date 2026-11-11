# slip_check.py - compare what the wheels say with what really happened, to find slip and bad calibration
import math

TICKS_PER_REV = 540
DIAMETER_USED_M = 0.0660          # what the robot's program thinks the wheel diameter is
DIAMETER_TRUE_M = 0.06589         # what it really is (Chapter 16's calibration)

# a 10 m test drive on a hard floor, then a 2 m drive over a dusty patch where the wheels slipped
ticks_hard = 26093                # ticks counted on the 10 m drive
ticks_dusty = 6300                # ticks counted on the 2 m drive

for label, ticks, true_m in [("hard floor", ticks_hard, 10.0), ("dusty patch", ticks_dusty, 2.0)]:
    wheel_m = ticks / TICKS_PER_REV * math.pi * DIAMETER_USED_M
    rolled_true = ticks / TICKS_PER_REV * math.pi * DIAMETER_TRUE_M
    slip = (rolled_true - true_m) / rolled_true
    print(f"{label:11s}: the robot thinks {wheel_m:.3f} m, it really moved {true_m:.3f} m")
    print(f"             the wheel surface rolled {rolled_true:.3f} m, so slip = {slip:.1%}")

print(f"diameter error alone: {DIAMETER_USED_M / DIAMETER_TRUE_M - 1:+.2%} on every metre")
