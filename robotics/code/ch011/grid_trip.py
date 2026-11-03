# grid_trip.py - a robot on a grid follows its moves, one after the other
x = 0                        # the robot starts in the corner square (0, 0)
y = 0
print("start:        ", x, y)
x = x + 3                    # move 1: 3 squares east (to the right)
print("after 3 east: ", x, y)
y = y + 2                    # move 2: 2 squares north (up)
print("after 2 north:", x, y)
x = x + 1                    # move 3: 1 square east
print("after 1 east: ", x, y)
y = y + 1                    # move 4: 1 square north
print("after 1 north:", x, y)
