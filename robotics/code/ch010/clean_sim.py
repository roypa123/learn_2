# clean_sim.py - a tiny cleaning robot in an empty room: drive straight, bump, turn a random angle
import math
import random
random.seed(3)

room_w, room_h = 4.0, 3.0     # the room is 4 m by 3 m
cell = 0.05                   # we divide the floor into squares of 5 cm x 5 cm
cols, rows = int(room_w / cell), int(room_h / cell)    # 80 x 60 = 4,800 squares
robot_r = 0.10                # the robot is a circle with radius 10 cm (20 cm wide)
brush_r = 0.08                # the brush cleans a circle with radius 8 cm under the robot
speed = 0.2                   # m/s
dt = 0.1                      # 10 loops per second

clean = [[False] * cols for r in range(rows)]   # a table of squares: False = still dirty
x, y = 0.5, 0.5               # start near a corner (the charging dock)
heading = 30.0                # direction in degrees (0 = towards the right wall)
clean_count = 0

for step in range(30 * 60 * 10 + 1):         # 30 minutes, 10 loops per second
    # ACT + SENSE: try to drive forward one step; the bumper tells us if we would hit a wall
    new_x = x + speed * dt * math.cos(math.radians(heading))
    new_y = y + speed * dt * math.sin(math.radians(heading))
    bumped = new_x < robot_r or new_x > room_w - robot_r or new_y < robot_r or new_y > room_h - robot_r
    if bumped:
        heading = heading + random.uniform(90, 270)   # THINK: turn away by a random angle
    else:
        x, y = new_x, new_y
    # the brush cleans every square whose centre is under it
    for r in range(int((y - brush_r) / cell), int((y + brush_r) / cell) + 1):
        for c in range(int((x - brush_r) / cell), int((x + brush_r) / cell) + 1):
            cx, cy = (c + 0.5) * cell, (r + 0.5) * cell
            if (cx - x) ** 2 + (cy - y) ** 2 <= brush_r ** 2 and not clean[r][c]:
                clean[r][c] = True
                clean_count = clean_count + 1
    if step % (5 * 60 * 10) == 0:            # every 5 minutes
        print("after", step // 600, "min:", round(100 * clean_count / (cols * rows), 1), "% of the floor is clean")
