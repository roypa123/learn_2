# route_on_screen.py - watch Rover drive a route on the screen
import turtle

SCALE = 60                          # pixels per metre
route = "FFRFFLFRFF"                # the route from Chapter 20

screen = turtle.Screen()
screen.title("Rover route")
screen.mode("logo")                 # 0 = north, angles grow clockwise, like a compass

rover = turtle.Turtle()
rover.shape("turtle")
rover.color("orange")
rover.pensize(3)
rover.speed(3)

for letter in route:
    if letter == "F":
        rover.forward(SCALE)
    elif letter == "L":
        rover.left(90)
    elif letter == "R":
        rover.right(90)

x_px, y_px = rover.position()
print(f"Rover ended at ({x_px / SCALE:.1f}, {y_px / SCALE:.1f}) m, facing {rover.heading():.0f}")
screen.mainloop()                   # keep the window open until you close it
