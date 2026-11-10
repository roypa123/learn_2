# function_table.py - a lookup table whose values are functions
def forward(speed):
    """Both wheels go the same way."""
    return speed, speed


def spin_left(speed):
    """Wheels go opposite ways, half speed: Rover turns on the spot."""
    return -speed / 2, speed / 2


def stop(speed):
    """Ignore the speed: nothing moves."""
    return 0.0, 0.0


COMMANDS = {"forward": forward, "left": spin_left, "stop": stop}   # no brackets!

for word, speed in [("forward", 0.2), ("left", 0.4), ("stop", 0.3), ("jump", 0.1)]:
    action = COMMANDS.get(word, stop)      # an unknown word safely means stop
    left, right = action(speed)            # now we call it, with brackets
    print(f"{word:8} left {left:+.2f}  right {right:+.2f}")
