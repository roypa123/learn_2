# waypoints.py - a route as a list of [x, y] points: length, time and energy
SPEED_MS = 0.25
POWER_W = 3.78                       # Rover (Chapter 5)

route = [[0.0, 0.0], [2.0, 0.0], [2.0, 1.5], [4.0, 3.0]]    # a list of lists

total_m = 0.0
for i in range(len(route) - 1):      # one pass per pair of neighbouring points
    x1, y1 = route[i]                # unpack a point into two names (Chapter 14)
    x2, y2 = route[i + 1]
    leg_m = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    total_m += leg_m
    print(f"leg {i + 1}: ({x1}, {y1}) to ({x2}, {y2}) = {leg_m:.2f} m")

time_s = total_m / SPEED_MS
energy_wh = POWER_W * time_s / 3600
print(f"total {total_m:.2f} m | time {time_s:.0f} s | energy {energy_wh:.4f} Wh")
