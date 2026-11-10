# intercept.py - when does a moving arm catch a part on a moving belt?
ARM_START = 0.0
ARM_SPEED = 0.5
PART_START = 0.6
BELT_END = 1.5


def meet_time(arm_start, arm_speed, part_start, part_speed):
    if arm_speed <= part_speed:
        return None
    return (part_start - arm_start) / (arm_speed - part_speed)


print("belt speed  meet time (s)  meet position (m)  on the belt?")
for belt_speed in [0.10, 0.20, 0.25, 0.35, 0.45, 0.60]:
    t = meet_time(ARM_START, ARM_SPEED, PART_START, belt_speed)
    if t is None:
        print(f"{belt_speed:10.2f}  the arm can never catch it")
        continue
    x = ARM_START + ARM_SPEED * t
    print(f"{belt_speed:10.2f} {t:14.2f} {x:18.2f}  {x <= BELT_END}")

limit = ARM_SPEED * (1 - (PART_START - ARM_START) / (BELT_END - ARM_START))
print(f"fastest belt that still works: {limit:.2f} m/s")
