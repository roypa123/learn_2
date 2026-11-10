# drive_any_way.py - Rover drives in ANY direction, using sine and cosine
import rover_math

legs = [(90, 2.0), (45, 1.0), (0, 0.5), (200, 1.5)]     # (heading in degrees, metres)

x_m, y_m = 0.0, 0.0
for heading_deg, distance_m in legs:
    x_m, y_m = rover_math.move(x_m, y_m, heading_deg, distance_m)
    print(f"heading {heading_deg:3d}: at ({x_m:.3f}, {y_m:.3f})")

print("clamp from the module:", rover_math.clamp(9, 0, 5))
