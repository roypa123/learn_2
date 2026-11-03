# encoder.py - from encoder ticks to wheel turns and distance driven
ticks = 2000                 # the encoder counted 2,000 ticks (a whole number: an int)
ticks_per_turn = 540         # one full wheel turn gives 540 ticks
wheel_diameter = 0.065       # metres (a 65 mm wheel: a measurement, a float)
pi = 3.14159

full_turns = ticks // ticks_per_turn         # how many WHOLE turns
leftover = ticks % ticks_per_turn            # ticks of the turn that is not finished yet
turns = ticks / ticks_per_turn               # turns as a decimal number
circumference = pi * wheel_diameter          # metres the wheel rolls in one turn
distance = turns * circumference             # metres driven

print("full turns:", full_turns, "| leftover ticks:", leftover)
print("turns:", round(turns, 3))
print("wheel circumference:", round(circumference, 4), "m")
print("distance driven:", round(distance, 3), "m =", round(distance * 100, 1), "cm")
