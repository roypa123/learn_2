# wrap_angle.py - keep angles in a sensible range, and find the shortest turn
def wrap_360(angle):
    return angle % 360


def wrap_180(angle):
    return (angle + 180) % 360 - 180


def shortest_turn(heading, target):
    return wrap_180(target - heading)


print(" angle   0..360   -180..180")
for a in [0, 90, 180, 190, 359, 360, 725, -10, -190]:
    print(f"{a:6d} {wrap_360(a):8d} {wrap_180(a):11d}")

print()
print("heading  target   shortest turn (+ is left)")
for h, t in [(350, 10), (10, 350), (90, 270), (0, 179), (170, -170)]:
    print(f"{h:7d} {t:7d} {shortest_turn(h, t):12d}")
