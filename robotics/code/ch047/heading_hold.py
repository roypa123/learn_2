# heading_hold.py - a boat turns towards a new heading, with and without wrapping the error
def wrap_180(angle):
    return (angle + 180) % 360 - 180


GAIN = 0.5           # turn this fraction of the error each step
MAX_TURN = 15        # degrees per step, at most


def steer(heading, target, wrap):
    error = target - heading
    if wrap:
        error = wrap_180(error)
    turn = max(-MAX_TURN, min(MAX_TURN, GAIN * error))
    return (heading + turn) % 360, error


for wrap in [False, True]:
    heading = 350.0
    total = 0.0
    steps = []
    for step in range(8):
        new_heading, error = steer(heading, 20.0, wrap)
        total += abs(wrap_180(new_heading - heading))
        heading = new_heading
        steps.append(f"{heading:5.1f}")
    print(f"wrap={wrap!s:5}: headings {' '.join(steps)}   turned {total:.0f} degrees")
