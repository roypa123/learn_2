# gripper.py - how hard must two fingers squeeze so a part does not slip out?
G = 9.81
SAFETY = 2.0             # squeeze twice what the physics says, for oily parts and worn pads


def squeeze_needed(mass_kg, mu, accel_up=0.0):
    """Each finger's squeeze force so that friction from two fingers holds the part."""
    hold = mass_kg * (G + accel_up)          # friction must hold the weight AND give the acceleration
    return hold / (2 * mu)                   # two fingers, each giving at most mu x squeeze


parts = [("plastic cap", 0.05, 0.4), ("steel bracket", 0.8, 0.3), ("oily steel bracket", 0.8, 0.12), ("glass bottle", 0.6, 0.25)]
GRIPPER_MAX_N = 40.0
print("part                 mass   mu    still      lifting at 5 m/s^2   with safety x2")
for name, m, mu in parts:
    still = squeeze_needed(m, mu)
    lifting = squeeze_needed(m, mu, 5.0)
    design = SAFETY * lifting
    verdict = "ok" if design <= GRIPPER_MAX_N else "TOO HEAVY for this gripper"
    print(f"{name:20s} {m:4.2f} kg  {mu:4.2f}  {still:6.2f} N   {lifting:8.2f} N   {design:12.2f} N  {verdict}")
