# fleet_move.py - one function moving many robots, each with its own state
def new_robot(name, x_m=0.0, speed_ms=0.2):
    """Return a dictionary describing a new robot."""
    return {"name": name, "x_m": x_m, "speed_ms": speed_ms, "odometer_m": 0.0}


def step(robot, dt_s):
    """Move one robot forward by one time step. Changes the dictionary."""
    moved = robot["speed_ms"] * dt_s
    robot["x_m"] += moved
    robot["odometer_m"] += abs(moved)


fleet = [new_robot("rover"), new_robot("cart", x_m=5.0, speed_ms=-0.1), new_robot("fast", speed_ms=0.5)]

for _ in range(10):                 # ten time steps
    for robot in fleet:
        step(robot, 0.5)

for robot in fleet:
    print(f"{robot['name']:6} x = {robot['x_m']:5.2f} m   driven {robot['odometer_m']:.2f} m")
