# grid_trip_b.py - the SAME four moves as grid_trip.py, in a different order
x = 0
y = 0
print("start:        ", x, y)
y = y + 2                    # 2 north first
print("after 2 north:", x, y)
x = x + 3                    # then 3 east
print("after 3 east: ", x, y)
y = y + 1                    # then 1 north
print("after 1 north:", x, y)
x = x + 1                    # then 1 east
print("after 1 east: ", x, y)
