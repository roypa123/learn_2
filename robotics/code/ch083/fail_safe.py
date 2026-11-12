# fail_safe.py - normally-open or normally-closed bumper switch: what happens when a wire breaks?
# with a pull-up: a closed switch to ground reads 0, an open switch (or a broken wire) reads 1


def pin(contact_closed, wire_ok=True):
    if not wire_ok:
        return 1                      # a broken wire is just an open circuit: the pull-up wins
    return 0 if contact_closed else 1


def no_bumper(hit, wire_ok=True):
    """Normally-open: the contacts close when the bumper is hit. Pin 0 means 'hit'."""
    return "HIT" if pin(contact_closed=hit, wire_ok=wire_ok) == 0 else "clear"


def nc_bumper(hit, wire_ok=True):
    """Normally-closed: the contacts open when the bumper is hit. Pin 1 means 'hit'."""
    return "HIT" if pin(contact_closed=not hit, wire_ok=wire_ok) == 1 else "clear"


print(f"{'situation':34s} {'normally-open':>14s} {'normally-closed':>16s}")
for label, hit, ok in [("no obstacle, wiring fine", False, True), ("robot hits a wall, wiring fine", True, True),
                       ("no obstacle, wire broken", False, False), ("robot hits a wall, wire broken", True, False)]:
    print(f"{label:34s} {no_bumper(hit, ok):>14s} {nc_bumper(hit, ok):>16s}")
print()
print("normally-open + broken wire: the robot never knows it hit something (unsafe, and silent)")
print("normally-closed + broken wire: the robot thinks it hit something and stops (safe, and you notice)")
