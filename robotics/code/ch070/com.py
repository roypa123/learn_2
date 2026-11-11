# com.py - the centre of mass of a robot made of parts, in two directions (forwards x and up z)
parts = [
    # name,             mass kg, x m (forward of the axle), z m (above the floor)
    ("chassis",          1.20,   -0.02,  0.06),
    ("battery",          0.90,   -0.06,  0.04),
    ("motors + wheels",  0.80,    0.00,  0.03),
    ("computer",         0.30,   -0.03,  0.10),
    ("arm (folded)",     0.80,    0.02,  0.18),
]


def centre_of_mass(parts):
    total = sum(m for name, m, x, z in parts)
    x_com = sum(m * x for name, m, x, z in parts) / total
    z_com = sum(m * z for name, m, x, z in parts) / total
    return total, x_com, z_com


m, x, z = centre_of_mass(parts)
print(f"arm folded:   mass {m:.2f} kg, centre of mass x = {x:+.3f} m, height = {z:.3f} m")

# the arm reaches forward and lifts a 0.5 kg box: its mass moves, and a new mass is added
reaching = [p for p in parts if p[0] != "arm (folded)"] + [("arm (reaching)", 0.80, 0.20, 0.22), ("box", 0.50, 0.38, 0.25)]
m, x, z = centre_of_mass(reaching)
print(f"arm reaching: mass {m:.2f} kg, centre of mass x = {x:+.3f} m, height = {z:.3f} m")

FRONT_WHEEL_X = 0.10           # the front caster
REAR_EDGE_X = -0.12            # the back wheels' contact line
print(f"support from x = {REAR_EDGE_X} to {FRONT_WHEEL_X} m: "
      f"{'stable' if REAR_EDGE_X < x < FRONT_WHEEL_X else 'TIPS OVER'} with the arm reaching")
