# coast_down.py - find the rolling resistance from how quickly the cart slows down on a flat floor
from ramp_data import FPS, FLAT_MARKS, CART_MASS_KG, WHEEL_MASS_KG

G = 9.81

# average speed between neighbouring marks, placed at the middle time of that gap (Chapter 57)
mid_t, speeds = [], []
for (s0, f0), (s1, f1) in zip(FLAT_MARKS, FLAT_MARKS[1:]):
    t0, t1 = f0 / FPS, f1 / FPS
    mid_t.append((t0 + t1) / 2)
    speeds.append((s1 - s0) / (t1 - t0))

# the straight line through the middle of the points: slope = sum((t - tm)(v - vm)) / sum((t - tm)^2)
tm = sum(mid_t) / len(mid_t)
vm = sum(speeds) / len(speeds)
slope = sum((t - tm) * (v - vm) for t, v in zip(mid_t, speeds)) / sum((t - tm) ** 2 for t in mid_t)
print("  middle time (s)   speed (m/s)")
for t, v in zip(mid_t, speeds):
    print(f"  {t:13.3f}   {v:10.3f}")
print(f"best straight line: speed falls by {-slope:.3f} m/s every second")

k = 4 * 0.5 * WHEEL_MASS_KG / CART_MASS_KG      # spinning wheels: 4 discs, each adds half its mass (Chapter 66)
c_rr = -slope * (1 + k) / G                       # rolling resistance m g c_rr = (m + extra) x deceleration
print(f"wheel factor k = {k:.3f}")
print(f"rolling resistance coefficient C_rr = {c_rr:.4f}")
