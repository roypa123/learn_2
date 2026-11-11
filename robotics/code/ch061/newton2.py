# newton2.py - Newton's second law: net force = mass x acceleration
MASS_KG = 4.0            # Rover with its battery

print("force needed for each acceleration (Rover, 4.0 kg):")
for a in [0.25, 0.5, 1.0, 2.0]:
    print(f"  a = {a:4.2f} m/s^2  needs  F = {MASS_KG * a:4.1f} N")

print("acceleration from a 2.0 N net force, for different masses:")
for m in [2.0, 4.0, 8.0, 25.0]:
    print(f"  m = {m:4.1f} kg  ->  a = {2.0 / m:5.3f} m/s^2")

forces = {"motors forwards": 3.0, "rolling resistance": -0.6, "air": -0.1}
net = sum(forces.values())
print("forces along the floor:", forces)
print(f"net force {net:+.1f} N, so a = {net / MASS_KG:.3f} m/s^2")
