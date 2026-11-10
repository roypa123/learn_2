# lawnmower.py - draw a cleaning robot's back-and-forth path in a room
import turtle

SCALE = 60                          # pixels per metre
WIDTH_M, HEIGHT_M = 8.0, 4.0        # the room
ROW_M = 0.5                         # the width of the strip cleaned on each pass

screen = turtle.Screen()
screen.mode("logo")
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)


def draw_room():
    """Draw the walls, with the bottom-left corner at (0, 0)."""
    pen.penup()
    pen.goto(0, 0)
    pen.setheading(0)
    pen.pendown()
    for side_m in [HEIGHT_M, WIDTH_M, HEIGHT_M, WIDTH_M]:
        pen.forward(side_m * SCALE)
        pen.right(90)


def draw_path():
    """Drive up and down the room. Return the number of passes and the length."""
    passes = int(WIDTH_M / ROW_M)
    length_m = 0.0
    pen.color("blue")
    pen.penup()
    pen.goto(ROW_M / 2 * SCALE, 0.1 * SCALE)
    pen.pendown()
    for i in range(passes):
        y_end_m = HEIGHT_M - 0.1 if i % 2 == 0 else 0.1      # up on even passes, down on odd
        x_m = ROW_M / 2 + i * ROW_M
        pen.goto(x_m * SCALE, y_end_m * SCALE)
        length_m += HEIGHT_M - 0.2
        if i < passes - 1:
            pen.goto((x_m + ROW_M) * SCALE, y_end_m * SCALE)
            length_m += ROW_M
    return passes, length_m


draw_room()
passes, length_m = draw_path()
print(f"{passes} passes, {length_m:.1f} m of driving, {length_m / 0.25 / 60:.1f} minutes at 0.25 m/s")
screen.mainloop()
