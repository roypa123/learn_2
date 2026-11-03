# wall_check.py - Rover drives towards a wall; run it with "python -i" and look at the variables afterwards
distance = 1.0               # metres from the wall
speed = 0.25                 # m/s
step_time = 0.5              # seconds per loop
for step in range(4):
    distance = distance - speed * step_time
print("done")
