# drone_range.py - how far out can a drone fly and still come home?
BATTERY_WH = 74
USABLE = 0.80
FLY_W = 180
HOVER_W = 200
SPEED_MS = 12

energy_j = BATTERY_WH * USABLE * 3600


def max_distance_m(hover_s):
    return (energy_j - HOVER_W * hover_s) * SPEED_MS / (2 * FLY_W)


print(f"usable energy: {energy_j:.0f} J")
print("hover (s)  furthest delivery (km)")
for hover_s in [0, 60, 120, 300, 600, 1100]:
    d = max_distance_m(hover_s)
    print(f"{hover_s:9d} {d / 1000:18.2f}")
