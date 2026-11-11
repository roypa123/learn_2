# two_link_ik.py - the joint angles a two-link arm needs to reach a point (law of cosines)
import math

UPPER_M = 0.40
FORE_M = 0.25


def solve_arm(x, y, elbow_up=True):
    d = math.hypot(x, y)
    if d > UPPER_M + FORE_M or d < abs(UPPER_M - FORE_M):
        return None
    inside_elbow = math.acos((UPPER_M ** 2 + FORE_M ** 2 - d ** 2) / (2 * UPPER_M * FORE_M))
    bend = math.pi - inside_elbow
    at_shoulder = math.acos((UPPER_M ** 2 + d ** 2 - FORE_M ** 2) / (2 * UPPER_M * d))
    direction = math.atan2(y, x)
    if elbow_up:
        return direction + at_shoulder, -bend
    return direction - at_shoulder, bend


def tip(shoulder, elbow):
    ex = UPPER_M * math.cos(shoulder)
    ey = UPPER_M * math.sin(shoulder)
    return ex + FORE_M * math.cos(shoulder + elbow), ey + FORE_M * math.sin(shoulder + elbow)


for target in [(0.30, 0.40), (0.60, 0.20), (0.5, 0.5)]:
    for up in [True, False]:
        answer = solve_arm(target[0], target[1], up)
        if answer is None:
            print(f"{target}: out of reach")
            break
        s, e = answer
        tx, ty = tip(s, e)
        print(f"{target} elbow {'up  ' if up else 'down'}: shoulder {math.degrees(s):7.2f}, "
              f"elbow {math.degrees(e):7.2f}  -> tip ({tx:.3f}, {ty:.3f})")
