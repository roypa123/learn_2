# launcher.py - will a parcel thrown by a sorting robot land in the bin?
from quadratic import solve_quadratic

G = 9.81
START_HEIGHT = 0.5      # m, where the parcel leaves the robot
UP_SPEED = 4.0          # m/s, upward part of the throw
ACROSS_SPEED = 2.4      # m/s, sideways part of the throw
BIN_TOP = 0.3           # m, height of the top of the bin
BIN_NEAR = 1.85         # m, near edge of the bin
BIN_FAR = 2.15          # m, far edge of the bin

top_time = UP_SPEED / G
top_height = START_HEIGHT + UP_SPEED * top_time - 0.5 * G * top_time ** 2

a = -0.5 * G
b = UP_SPEED
c = START_HEIGHT - BIN_TOP
land_time = max(solve_quadratic(a, b, c))
land_x = ACROSS_SPEED * land_time

print(f"highest point : {top_height:.3f} m after {top_time:.3f} s")
print(f"reaches bin height after {land_time:.3f} s, at x = {land_x:.3f} m")
print("in the bin!" if BIN_NEAR <= land_x <= BIN_FAR else "missed the bin")
