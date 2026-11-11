# inertia.py - moment of inertia: I = sum of (mass x distance squared), and tau = I x alpha
# 1) the same 1 kg, placed at different distances from the axis
for r in [0.1, 0.2, 0.4]:
    print(f"1 kg at {r:.1f} m: I = {1.0 * r ** 2:.3f} kg m^2")

# 2) a dumbbell robot arm: two masses on a light bar, turning about the shoulder
masses = [(0.15, 0.10), (0.15, 0.30), (0.25, 0.50)]     # (mass in kg, distance in m)
I = 0
for m, r in masses:
    I = I + m * r ** 2
print(f"arm made of point masses: I = {I:.4f} kg m^2")

# 3) common shapes, each 0.40 kg
M, L, R = 0.40, 0.50, 0.10
print(f"rod {L} m long, turning about its end:    I = M L^2 / 3  = {M * L ** 2 / 3:.4f} kg m^2")
print(f"rod {L} m long, turning about its middle: I = M L^2 / 12 = {M * L ** 2 / 12:.4f} kg m^2")
print(f"solid disc of radius {R} m:               I = M R^2 / 2  = {M * R ** 2 / 2:.4f} kg m^2")
print(f"thin ring of radius {R} m:                I = M R^2      = {M * R ** 2:.4f} kg m^2")

# 4) tau = I alpha: the same torque on the rod about its end and about its middle
TORQUE = 0.5
for name, i in [("end", M * L ** 2 / 3), ("middle", M * L ** 2 / 12)]:
    print(f"0.5 N m on the rod about its {name}: alpha = {TORQUE / i:.1f} rad/s^2")
