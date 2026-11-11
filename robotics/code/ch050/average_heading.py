# average_heading.py - the average of compass readings near north, done wrongly and rightly
import math

readings_deg = [350, 355, 2, 8, 5, 352]

plain = sum(readings_deg) / len(readings_deg)

sum_x = sum(math.cos(math.radians(d)) for d in readings_deg)
sum_y = sum(math.sin(math.radians(d)) for d in readings_deg)
vector = math.degrees(math.atan2(sum_y, sum_x)) % 360
spread = math.hypot(sum_x, sum_y) / len(readings_deg)

print("readings     :", readings_deg)
print(f"plain average: {plain:.1f} degrees")
print(f"vector mean  : {vector:.1f} degrees")
print(f"agreement    : {spread:.4f}  (1 = all readings the same)")
