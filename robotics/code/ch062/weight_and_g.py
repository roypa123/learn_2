# weight_and_g.py - the same mass has a different weight on different worlds, and g falls with height
BIG_G = 6.674e-11            # the gravitational constant, N m^2 / kg^2
EARTH_MASS_KG = 5.972e24
EARTH_RADIUS_M = 6.371e6

ROVER_MASS_KG = 4.0
worlds = {"Earth": 9.81, "Moon": 1.62, "Mars": 3.71}
for name, g in worlds.items():
    print(f"on {name:5s}: mass {ROVER_MASS_KG} kg, weight {ROVER_MASS_KG * g:5.2f} N")

g_surface = BIG_G * EARTH_MASS_KG / EARTH_RADIUS_M ** 2
print(f"g from Newton's law of gravity: {g_surface:.2f} m/s^2")

for height_km in [0, 10, 100, 400, 36000]:
    r = EARTH_RADIUS_M + height_km * 1000
    g = BIG_G * EARTH_MASS_KG / r ** 2
    print(f"{height_km:6d} km up: g = {g:5.2f} m/s^2 ({g / g_surface:.0%} of the surface value)")
