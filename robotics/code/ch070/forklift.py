# forklift.py - how heavy a load can a forklift robot carry, and how hard may it brake with it held high?
G = 9.81
ROBOT_KG = 400.0
ROBOT_COM_BEHIND = 0.50     # m, the robot's own centre of mass behind the front wheels
ROBOT_COM_HEIGHT = 0.45     # m
LOAD_AHEAD = 0.40           # m, the load's centre of mass in front of the front wheels

# standing still: about the front wheels, load x 0.40 must stay below robot x 0.50
max_load = ROBOT_KG * ROBOT_COM_BEHIND / LOAD_AHEAD
print(f"standing still, the heaviest load is {max_load:.0f} kg (with no margin at all)")

LOAD_KG = 300.0
print(f"with a {LOAD_KG:.0f} kg load, braking limits (tipping forward over the front wheels):")
for lift_m in [0.2, 1.0, 2.0, 3.0]:
    load_height = lift_m + 0.3                       # the load's centre is 0.3 m above the forks
    # tipping happens when the braking torques beat the gravity torques, both about the front wheels
    gravity_moment = ROBOT_KG * G * ROBOT_COM_BEHIND - LOAD_KG * G * LOAD_AHEAD
    braking_per_a = ROBOT_KG * ROBOT_COM_HEIGHT + LOAD_KG * load_height
    a_max = gravity_moment / braking_per_a
    print(f"  forks at {lift_m:.1f} m: brake at most {a_max:.2f} m/s^2")
