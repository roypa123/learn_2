# crash_demo.py - a crash passes through three functions: read the traceback
def trip_time(route_m, speed_ms):
    return route_m / speed_ms


def report(route_m, speed_ms):
    seconds = trip_time(route_m, speed_ms)
    print("trip takes", seconds, "s")


def main():
    report(900, 1.257)
    report(900, 0)


main()
