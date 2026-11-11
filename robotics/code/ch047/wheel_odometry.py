# wheel_odometry.py - distance rolled = radius x angle turned (in radians)
import math

TICKS_PER_TURN = 540            # Rover's encoder (Chapter 23)
WHEEL_RADIUS_M = 0.06589 / 2    # half the calibrated diameter (Chapter 16)

print("  ticks   turns   angle (rad)   distance (m)")
for ticks in [135, 540, 1000, 2640]:
    turns = ticks / TICKS_PER_TURN
    angle_rad = turns * 2 * math.pi
    distance = WHEEL_RADIUS_M * angle_rad
    print(f"{ticks:7d} {turns:7.3f} {angle_rad:13.3f} {distance:14.4f}")

wheel_rpm = 120
omega = wheel_rpm * 2 * math.pi / 60
print(f"{wheel_rpm} rpm = {omega:.3f} rad/s -> robot speed {omega * WHEEL_RADIUS_M:.3f} m/s")
