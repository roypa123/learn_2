# grip_limits.py - the fastest a robot may speed up or brake before its wheels or its load slip
G = 9.81
SPEED = 1.5                    # m/s
REACTION_S = 0.3

floors = {"dry concrete": 0.8, "dusty floor": 0.5, "wet tiles": 0.3, "icy floor": 0.1}
TOTE_MU = 0.2                  # plastic tote on the robot's steel top

print("floor          wheel limit   braking distance   stopping distance")
for name, mu in floors.items():
    a_max = mu * G                                   # every wheel braked: friction mu m g, so a = mu g
    braking = SPEED ** 2 / (2 * a_max)               # Chapter 59
    print(f"{name:14s} {a_max:6.2f} m/s^2   {braking:10.3f} m   {SPEED * REACTION_S + braking:12.3f} m")

print(f"the tote slides if the robot accelerates or brakes harder than {TOTE_MU * G:.2f} m/s^2")
print(f"so on dry concrete the tote, not the wheels, sets the limit: brake at most {TOTE_MU * G:.2f} m/s^2")
print(f"braking distance with the tote limit: {SPEED ** 2 / (2 * TOTE_MU * G):.3f} m")
