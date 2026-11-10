# drive_with_keys.py - drive a robot on the screen with the arrow keys
import turtle

STEP_PX = 20
TURN_DEG = 15
LIMIT_PX = 200                     # the edge of the arena

screen = turtle.Screen()
screen.mode("logo")
screen.title("Arrow keys drive. Close the window to stop.")

rover = turtle.Turtle()
rover.shape("turtle")
rover.color("orange")
rover.speed(0)


def inside(x, y):
    """Return True if this point is inside the arena."""
    return abs(x) <= LIMIT_PX and abs(y) <= LIMIT_PX


def forward():
    rover.forward(STEP_PX)
    x, y = rover.position()
    if not inside(x, y):            # a wall: undo the move
        rover.backward(STEP_PX)
        print("bump!")


def turn_left():
    rover.left(TURN_DEG)


def turn_right():
    rover.right(TURN_DEG)


screen.onkey(forward, "Up")         # a function name, with no brackets (Chapter 23)
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")
screen.listen()                     # start paying attention to the keyboard
screen.mainloop()
