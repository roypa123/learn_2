# route_runner.py - Rover follows a route written as a string of letters
route = "FFRFFLFRFF"                # F = forward 1 m, L = turn left, R = turn right

x_m, y_m = 0, 0                     # STATE: position on the grid
heading = 0                         # STATE: 0 = north, 1 = east, 2 = south, 3 = west
moves = 0                           # a counter

for letter in route:                # one pass for each letter
    if letter == "L":
        heading = (heading - 1) % 4     # % keeps it between 0 and 3 (Chapter 13)
    elif letter == "R":
        heading = (heading + 1) % 4
    elif letter == "F":
        if heading == 0:
            y_m += 1
        elif heading == 1:
            x_m += 1
        elif heading == 2:
            y_m -= 1
        else:
            x_m -= 1
        moves += 1
    print(f"{letter}: at ({x_m}, {y_m}) facing {heading}")

print("driven:", moves, "m | straight-line distance:", round((x_m ** 2 + y_m ** 2) ** 0.5, 2), "m")
