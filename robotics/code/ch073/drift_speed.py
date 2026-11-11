# drift_speed.py - how fast do the electrons themselves move in a wire? (slowly!)
ELECTRON_C = 1.602e-19       # charge of one electron, C
FREE_PER_M3 = 8.5e28         # free electrons in one cubic metre of copper


def drift_speed(current_a, area_mm2):
    """Average speed of the electrons in a copper wire, in metres per second."""
    area_m2 = area_mm2 * 1e-6                           # 1 mm^2 = 0.000001 m^2
    return current_a / (FREE_PER_M3 * ELECTRON_C * area_m2)


print(f"{'wire':28s} {'current':>8s} {'area':>8s} {'drift':>12s} {'time for 1 m':>14s}")
cases = [
    ("Rover, normal driving", 0.53, 0.5),
    ("Rover, motors starting", 3.1, 0.5),
    ("house wire, 1 A", 1.0, 1.0),
    ("drone motor wire, hover", 25.0, 4.0),
]
for name, current, area in cases:
    v = drift_speed(current, area)
    print(f"{name:28s} {current:6.2f} A {area:4.1f} mm2 {v * 1000:9.3f} mm/s {1 / v / 3600:10.2f} h")

print()
print("but the push travels along the wire at about 200,000,000 m/s,")
print(f"so a 1 m wire passes the message in {1 / 2e8 * 1e9:.0f} nanoseconds")
