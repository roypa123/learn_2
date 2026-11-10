# command_table.py - turn command words into wheel speeds with a lookup table
SPEED_MS = 0.2

COMMANDS = {                 # word: (left wheel, right wheel), as fractions of full speed
    "forward": (1.0, 1.0),
    "back":    (-1.0, -1.0),
    "left":    (-0.5, 0.5),
    "right":   (0.5, -0.5),
    "stop":    (0.0, 0.0),
}

script = ["forward", "left", "FORWARD", "jump", "stop"]

for raw in script:
    word = raw.strip().lower()
    if word in COMMANDS:
        left, right = COMMANDS[word]     # unpack the tuple into two names
        print(f"{word:8} left {left * SPEED_MS:+.2f}  right {right * SPEED_MS:+.2f} m/s")
    else:
        print(f"{word:8} unknown: motors stay stopped")
