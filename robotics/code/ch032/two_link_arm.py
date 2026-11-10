# two_link_arm.py - draw a two-link robot arm for any pair of joint angles
import math
import turtle

SCALE = 300                         # pixels per metre
UPPER_M, FORE_M = 0.3, 0.2


def elbow_and_tip(shoulder_deg, elbow_deg):
    """Return the (x, y) of the elbow and of the tip. Angles from the x axis."""
    a = math.radians(shoulder_deg)
    b = math.radians(shoulder_deg + elbow_deg)
    ex, ey = UPPER_M * math.cos(a), UPPER_M * math.sin(a)
    tx, ty = ex + FORE_M * math.cos(b), ey + FORE_M * math.sin(b)
    return (ex, ey), (tx, ty)


def draw_arm(pen, shoulder_deg, elbow_deg, colour):
    elbow, tip = elbow_and_tip(shoulder_deg, elbow_deg)
    pen.color(colour)
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()
    pen.goto(elbow[0] * SCALE, elbow[1] * SCALE)
    pen.dot(10)
    pen.goto(tip[0] * SCALE, tip[1] * SCALE)
    pen.dot(14)
    return tip


screen = turtle.Screen()
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.pensize(5)

for shoulder, elbow, colour in [(30, 45, "blue"), (60, -30, "green"), (100, 60, "red")]:
    tip_x, tip_y = draw_arm(pen, shoulder, elbow, colour)
    print(f"shoulder {shoulder:3d}, elbow {elbow:3d}: tip at ({tip_x:.3f}, {tip_y:.3f}) m")

screen.mainloop()
