# pin_planner.py - give each of Rover's wires a pin on the Arduino Uno, following the rules of each pin
PINS = {                                   # Uno pin: what it can do
    0: {"usb"}, 1: {"usb"},                # pins 0 and 1 carry USB serial: keep them free
    2: {"in", "out", "interrupt"}, 3: {"in", "out", "interrupt", "pwm"},
    4: {"in", "out"}, 5: {"in", "out", "pwm"}, 6: {"in", "out", "pwm"}, 7: {"in", "out"}, 8: {"in", "out"},
    9: {"in", "out", "pwm"}, 10: {"in", "out", "pwm"}, 11: {"in", "out", "pwm"}, 12: {"in", "out"},
    13: {"out"},                           # the board's "L" LED hangs on pin 13: use it only as an output
    "A0": {"in", "out", "analog"}, "A1": {"in", "out", "analog"}, "A2": {"in", "out", "analog"},
    "A3": {"in", "out", "analog"}, "A4": {"in", "out", "analog", "i2c"}, "A5": {"in", "out", "analog", "i2c"},
}
NEEDS = [                                  # (what Rover connects, the kind of pin it needs)
    ("left encoder A", "interrupt"), ("right encoder A", "interrupt"),
    ("IMU SDA", "i2c"), ("IMU SCL", "i2c"),
    ("line sensor L", "analog"), ("line sensor M", "analog"), ("line sensor R", "analog"), ("battery voltage", "analog"),
    ("left motor speed", "pwm"), ("right motor speed", "pwm"),
    ("left encoder B", "in"), ("right encoder B", "in"), ("left bumper", "in"), ("right bumper", "in"),
    ("ultrasonic echo", "in"), ("ultrasonic trigger", "out"), ("status LED", "out"),
    ("left motor IN1", "out"), ("left motor IN2", "out"),
    ("right motor IN1", "out"), ("right motor IN2", "out"), ("driver standby", "out"),
]

free = dict(PINS)
plan, missing = [], []
for name, kind in NEEDS:                   # the rarest kinds come first in NEEDS, so they get first choice
    choices = [p for p, can in free.items() if kind in can]
    choices.sort(key=lambda p: len(free[p]))       # take the pin that can do the fewest other things
    if choices:
        pin = choices[0]
        plan.append((name, kind, pin))
        del free[pin]
    else:
        missing.append(name)

for name, kind, pin in plan:
    print(f"{name:20s} {kind:10s} -> pin {pin}")
print(f"\nused {len(plan)} pins; left free: {[p for p in free if 'usb' not in free[p]]}")
if missing:
    print(f"NOT ENOUGH PINS for {len(missing)} needs: {', '.join(missing)}")
