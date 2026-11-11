# ramp_data.py - the measurements from the ramp project (one example set; replace them with your own)
FPS = 30                       # the phone video's frames per second

# the cart and the ramp, measured with a kitchen scale and a tape measure
CART_MASS_KG = 0.250           # the whole cart, wheels included
WHEEL_MASS_KG = 0.010          # each of the 4 wheels
WHEEL_RADIUS_M = 0.015
RAMP_LENGTH_M = 1.20
RAMP_RISE_M = 0.15             # how much higher the top end is than the bottom end

# run 1, down the ramp: (distance from the start line in m, video frame when the cart's nose passed it)
# frame 0 is the frame where the cart was let go
RAMP_MARKS = [(0.1, 14), (0.2, 20), (0.3, 24), (0.4, 28), (0.5, 31), (0.6, 34),
              (0.7, 36), (0.8, 39), (0.9, 41), (1.0, 43), (1.1, 46), (1.2, 48)]

# run 2, coasting on the flat floor after a push: marks every 0.2 m, frame 0 at the first line
FLAT_MARKS = [(0.0, 0), (0.2, 6), (0.4, 13), (0.6, 19), (0.8, 26), (1.0, 34),
              (1.2, 41), (1.4, 50), (1.6, 60), (1.8, 70), (2.0, 82)]

if __name__ == "__main__":
    print(f"{len(RAMP_MARKS)} ramp marks, {len(FLAT_MARKS)} flat marks, video at {FPS} frames per second")
    print(f"ramp angle: sin = {RAMP_RISE_M / RAMP_LENGTH_M:.4f}")
