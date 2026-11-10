# route_function.py - Chapter 20's route follower, now reusable
def run_route(route):
    """Follow a route of F, L and R. Return (x, y, heading)."""
    x, y, heading = 0, 0, 0
    for letter in route:
        if letter == "L":
            heading = (heading - 1) % 4
        elif letter == "R":
            heading = (heading + 1) % 4
        elif letter == "F":
            if heading == 0:
                y += 1
            elif heading == 1:
                x += 1
            elif heading == 2:
                y -= 1
            else:
                x -= 1
    return x, y, heading


print(run_route("FFRFFLFRFF"))
print(run_route("FRFRFRFR"))
print(run_route(""))
