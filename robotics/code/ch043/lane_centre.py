# lane_centre.py - where are the lane lines at the bottom of the camera image?
IMAGE_WIDTH = 640
BOTTOM_ROW = 479
METRES_PER_PIXEL = 0.004       # at the bottom of the image, from a calibration


def x_at_row(p, q, row):
    a = (q[0] - p[0]) / (q[1] - p[1])     # change in x for each row down
    b = p[0] - a * p[1]
    return a * row + b


left = ((210, 300), (90, 470))
right = ((430, 300), (560, 470))

left_x = x_at_row(left[0], left[1], BOTTOM_ROW)
right_x = x_at_row(right[0], right[1], BOTTOM_ROW)
lane_centre = (left_x + right_x) / 2
image_centre = IMAGE_WIDTH / 2
offset_px = image_centre - lane_centre

print(f"left line at the bottom : x = {left_x:.1f}")
print(f"right line at the bottom: x = {right_x:.1f}")
print(f"lane centre             : x = {lane_centre:.1f}")
print(f"camera centre           : x = {image_centre:.1f}")
print(f"car is {offset_px:+.1f} px = {offset_px * METRES_PER_PIXEL:+.3f} m from the lane centre")
