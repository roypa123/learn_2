# stereo_range.py - two cameras a known distance apart both see the same object
import math

BASELINE_M = 0.20          # distance between the two cameras

sightings = [(80.0, 85.0), (88.0, 89.0), (70.0, 72.0)]   # angles at the left and right camera, in degrees

print(" left  right  angle at object   distance from left   position (x, y)")
for left_deg, right_deg in sightings:
    at_object = 180.0 - left_deg - right_deg
    from_left = BASELINE_M * math.sin(math.radians(right_deg)) / math.sin(math.radians(at_object))
    x = from_left * math.cos(math.radians(left_deg))
    y = from_left * math.sin(math.radians(left_deg))
    print(f"{left_deg:5.1f} {right_deg:6.1f} {at_object:12.1f} {from_left:18.3f} m     ({x:.3f}, {y:.3f})")
