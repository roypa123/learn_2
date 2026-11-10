# go_to_goal.py - which way must Rover turn, and how far is the goal?
import math
from rover_math import heading_error

goal_x, goal_y = 3.0, 4.0
x_m, y_m = 1.0, 1.0
heading_deg = 90.0                     # Rover faces east

dx = goal_x - x_m
dy = goal_y - y_m
distance_m = math.hypot(dx, dy)
bearing_deg = math.degrees(math.atan2(dx, dy)) % 360     # compass bearing of the goal
turn_deg = heading_error(bearing_deg, heading_deg)

print(f"distance to goal: {distance_m:.3f} m")
print(f"goal is on bearing {bearing_deg:.1f} degrees")
print(f"turn by {turn_deg:+.1f} degrees ({'left' if turn_deg < 0 else 'right'})")
