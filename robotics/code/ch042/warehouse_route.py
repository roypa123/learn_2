# warehouse_route.py - how much driving do two visiting orders need on a grid?
CELL_M = 1.2


def grid_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def route_cells(start, stops):
    total = 0
    here = start
    for stop in stops:
        total = total + grid_distance(here, stop)
        here = stop
    return total


def nearest_first(start, stops):
    left = list(stops)
    ordered = []
    here = start
    while left:
        best = min(left, key=lambda stop: grid_distance(here, stop))
        ordered.append(best)
        left.remove(best)
        here = best
    return ordered


start = (0, 0)
orders = [(8, 2), (1, 7), (6, 6), (2, 1), (9, 9)]

as_given = route_cells(start, orders)
better = nearest_first(start, orders)
better_cells = route_cells(start, better)

print(f"orders as given: {as_given} cells = {as_given * CELL_M:.1f} m")
print(f"nearest first  : {better}")
print(f"nearest first  : {better_cells} cells = {better_cells * CELL_M:.1f} m")
