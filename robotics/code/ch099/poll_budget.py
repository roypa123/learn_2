# poll_budget.py - how often must a robot look at a switch? Worst-case travel between two readings.
machines = [
    # (name, speed in mm per second)
    ("Rover driving into a wall", 300),
    ("3D printer head homing", 50),
    ("factory arm joint near its limit", 500),
]
loop_ms = [1, 10, 50, 200]                 # time between two readings of the switch

print(f"{'machine':34s}" + "".join(f"{f'{t} ms loop':>12s}" for t in loop_ms))
for name, speed in machines:
    extra = [speed * t / 1000 for t in loop_ms]      # distance moved while the switch is pressed but not yet read
    print(f"{name:34s}" + "".join(f"{e:9.1f} mm" for e in extra))
print()
for t in loop_ms:
    print(f"a {t:3d} ms loop is only sure to see a press that lasts longer than {t} ms")
