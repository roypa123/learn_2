# room_map.py - turn the measured room into a grid map, in the same text style as GridBot (Chapter 36)
import math

from room_survey import place_corners, shoelace_area
from survey_data import DIAGONALS, SIDES

CELL_M = 0.25


def inside(point, ring, area):
    pieces = 0.0
    for i in range(len(ring)):
        pieces += shoelace_area([point, ring[i], ring[(i + 1) % len(ring)]])
    return math.isclose(pieces, area, rel_tol=1e-9)


corners = place_corners(SIDES, DIAGONALS)
ring = [corners[k] for k in "ABCDE"]
area = shoelace_area(ring)
width = max(x for x, y in ring)
height = max(y for x, y in ring)
cols = math.ceil(width / CELL_M)
rows = math.ceil(height / CELL_M)

free = 0
lines = []
for row in range(rows - 1, -1, -1):
    text = ""
    for col in range(cols):
        centre = ((col + 0.5) * CELL_M, (row + 0.5) * CELL_M)
        if inside(centre, ring, area):
            text += "."
            free += 1
        else:
            text += "#"
    lines.append("#" + text + "#")

border = "#" * (cols + 2)
print("\n".join([border] + lines + [border]))
print(f"{cols} x {rows} cells of {CELL_M} m; {free} free cells = {free * CELL_M ** 2:.2f} m^2 (true area {area:.2f} m^2)")
