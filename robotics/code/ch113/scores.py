# scores.py - collect the reaction game's results from the Arduino with pyserial, and save and summarise them
# usage: python scores.py COM3        (the Arduino runs reaction_game.ino)
import csv
import sys
import time

import serial                                    # pyserial (Chapter 111)

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"
results = []                                     # (round, reaction in ms, or None for a false start / too slow)
with serial.Serial(PORT, 115200, timeout=1) as ser:
    time.sleep(2)                                # the Uno restarts when the port opens: a fresh game (Chapter 111)
    ser.reset_input_buffer()
    deadline = time.monotonic() + 40
    while time.monotonic() < deadline:
        line = ser.readline().decode("ascii", errors="replace").strip()
        if not line:
            continue
        print("  Arduino:", line)
        if line.startswith("best"):
            break
        parts = line.split(",")
        if len(parts) != 2 or not parts[0].isdigit():
            continue                             # the header line
        try:
            results.append((int(parts[0]), float(parts[1])))
        except ValueError:
            results.append((int(parts[0]), None))   # "false start" or "too slow"

with open("scores.csv", "w", newline="") as f:
    csv.writer(f).writerows([("round", "reaction_ms")] + [(r, "" if ms is None else ms) for r, ms in results])
good = [ms for _, ms in results if ms is not None]
print(f"rounds: {len(results)}, good: {len(good)}, false starts or too slow: {len(results) - len(good)}")
print(f"best {min(good):.1f} ms, worst {max(good):.1f} ms, average {sum(good) / len(good):.1f} ms")
