# world_and_cell.py - from metres on the floor to a square on the map, and back
import math

CELL_M = 0.05
ORIGIN_X = -2.0
ORIGIN_Y = -1.0
ROWS = 80
COLS = 120


def world_to_cell(x, y):
    col = math.floor((x - ORIGIN_X) / CELL_M)
    row = math.floor((y - ORIGIN_Y) / CELL_M)
    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None


def cell_to_world(row, col):
    x = ORIGIN_X + (col + 0.5) * CELL_M
    y = ORIGIN_Y + (row + 0.5) * CELL_M
    return x, y


for point in [(0.0, 0.0), (0.97, 0.13), (-2.0, -1.0), (3.99, 2.99), (4.0, 0.0)]:
    cell = world_to_cell(point[0], point[1])
    if cell is None:
        print(f"{point} is outside the map")
        continue
    back = cell_to_world(cell[0], cell[1])
    print(f"{point} -> cell {cell} -> centre ({back[0]:.3f}, {back[1]:.3f})")
