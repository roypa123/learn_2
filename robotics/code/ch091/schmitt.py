# schmitt.py - a slow, noisy edge read by a plain input and by a Schmitt-trigger input
import math
import random

random.seed(2)
DT = 1e-5
THRESHOLD = 2.5                 # a plain input switches at one voltage
UP, DOWN = 3.0, 2.0             # a Schmitt input: switch up only above 3.0 V, down only below 2.0 V

plain, schmitt = 0, 0
plain_changes, schmitt_changes = 0, 0
t = 0.0
while t < 0.02:
    clean = 5.0 / (1 + math.exp(-(t - 0.01) / 0.0015))          # a slow rise from 0 to 5 V (a line sensor crossing an edge)
    v = clean + random.gauss(0, 0.25)                            # plus noise from the motors
    new_plain = 1 if v > THRESHOLD else 0
    if new_plain != plain:
        plain_changes += 1
        plain = new_plain
    if schmitt == 0 and v > UP:
        schmitt, schmitt_changes = 1, schmitt_changes + 1
    elif schmitt == 1 and v < DOWN:
        schmitt, schmitt_changes = 0, schmitt_changes + 1
    t += DT
print(f"one slow rise with 0.25 V of noise, read every {DT * 1e6:.0f} us:")
print(f"  plain input (switches at {THRESHOLD} V): {plain_changes} changes")
print(f"  Schmitt input (up at {UP} V, down at {DOWN} V): {schmitt_changes} change")
