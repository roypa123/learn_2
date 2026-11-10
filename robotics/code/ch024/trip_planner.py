# trip_planner.py - plan a route with defaults, named arguments and several results
DEFAULT_SPEED_MS = 0.25
DEFAULT_POWER_W = 3.78


def distance(a, b):
    """Return the straight-line distance between two (x, y) points."""
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5


def route_length(route):
    """Return the total length of a list of (x, y) points."""
    total = 0.0
    for i in range(len(route) - 1):
        total += distance(route[i], route[i + 1])
    return total


def plan_trip(route, speed_ms=DEFAULT_SPEED_MS, power_w=DEFAULT_POWER_W):
    """Return (metres, seconds, watt-hours) for driving along a route."""
    metres = route_length(route)
    seconds = metres / speed_ms
    watt_hours = power_w * seconds / 3600
    return metres, seconds, watt_hours


route = [(0.0, 0.0), (2.0, 0.0), (2.0, 1.5), (4.0, 3.0)]

m, s, wh = plan_trip(route)
print(f"normal:     {m:.2f} m  {s:.0f} s  {wh:.4f} Wh")

m, s, wh = plan_trip(route, speed_ms=0.5)
print(f"fast:       {m:.2f} m  {s:.0f} s  {wh:.4f} Wh")

m, s, wh = plan_trip(route, power_w=8.78)
print(f"with Pi:    {m:.2f} m  {s:.0f} s  {wh:.4f} Wh")
