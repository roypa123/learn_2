# lawnmower.py - the same robot cleans in straight rows, like mowing a lawn (needs to know where it is)
room_w, room_h = 4.0, 3.0
cell = 0.05
cols, rows = int(room_w / cell), int(room_h / cell)
robot_r = 0.10
brush_r = 0.08
row_gap = 0.15                # distance between two rows (a little less than the brush width, 0.16 m)
speed = 0.2
dt = 0.1

# the plan: a list of corner points, left-right-up-right-left-up ... until the top wall
plan = []
y_row = robot_r
going_right = True
while y_row <= room_h - robot_r:
    if going_right:
        plan.append((robot_r, y_row))
        plan.append((room_w - robot_r, y_row))
    else:
        plan.append((room_w - robot_r, y_row))
        plan.append((robot_r, y_row))
    going_right = not going_right
    y_row = y_row + row_gap

clean = [[False] * cols for r in range(rows)]
clean_count = 0
x, y = plan[0]
target = 1                                    # index of the next corner point in the plan
step = 0
while target < len(plan):
    tx, ty = plan[target]
    dist = ((tx - x) ** 2 + (ty - y) ** 2) ** 0.5
    if dist <= speed * dt:                    # close enough: jump to the corner, aim at the next one
        x, y = tx, ty
        target = target + 1
    else:                                     # drive one step straight towards the corner
        x = x + speed * dt * (tx - x) / dist
        y = y + speed * dt * (ty - y) / dist
    for r in range(int((y - brush_r) / cell), int((y + brush_r) / cell) + 1):
        for c in range(int((x - brush_r) / cell), int((x + brush_r) / cell) + 1):
            cx, cy = (c + 0.5) * cell, (r + 0.5) * cell
            if (cx - x) ** 2 + (cy - y) ** 2 <= brush_r ** 2 and not clean[r][c]:
                clean[r][c] = True
                clean_count = clean_count + 1
    step = step + 1
    if step % 600 == 0:
        print("after", step // 600, "min:", round(100 * clean_count / (cols * rows), 1), "% clean")
print("finished after", round(step * dt / 60, 1), "min:", len(plan) // 2, "rows,", round(100 * clean_count / (cols * rows), 1), "% clean")
