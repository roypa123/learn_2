# coverage_grid.py - a cleaning robot's back-and-forth path, printed as a numbered map
WIDTH = 6                           # columns of floor cells
HEIGHT = 4                          # rows of floor cells

for row in range(HEIGHT):           # the outer loop: one row at a time
    line = ""
    for col in range(WIDTH):        # the inner loop: one cell at a time
        if row % 2 == 0:            # even rows run left to right
            order = row * WIDTH + col
        else:                       # odd rows run right to left
            order = row * WIDTH + (WIDTH - 1 - col)
        line += f"{order:4d}"
    print(line)

cells = WIDTH * HEIGHT
moves = cells - 1                   # each move reaches one new cell
print("cells:", cells, "| moves:", moves)
