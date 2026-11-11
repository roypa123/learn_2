# wheel_speeds.py - what must each wheel do to give this forward speed and turn rate?
import math

from solve_2x2 import solve_2x2

TRACK_M = 0.15            # distance between Rover's wheels (Chapter 35)
WHEEL_D_M = 0.06589       # wheel diameter (Chapter 16)

print(" forward   turn   |   left wheel   right wheel  (m/s)   left rpm  right rpm")
for v, w in [(0.3, 0.0), (0.3, 1.0), (0.0, 2.0), (0.2, -0.5)]:
    # 0.5 L + 0.5 R = v        and       -L/T + R/T = w
    left, right = solve_2x2(0.5, 0.5, v, -1 / TRACK_M, 1 / TRACK_M, w)
    rpm_left = left / (math.pi * WHEEL_D_M) * 60
    rpm_right = right / (math.pi * WHEEL_D_M) * 60
    print(f"{v:7.2f} {w:6.2f}   | {left:11.3f} {right:12.3f}        {rpm_left:9.1f} {rpm_right:9.1f}")
