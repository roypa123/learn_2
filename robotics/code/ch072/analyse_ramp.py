# analyse_ramp.py - turn the video frames into times, then find the cart's acceleration down the ramp
from ramp_data import FPS, RAMP_MARKS

times = [frame / FPS for s, frame in RAMP_MARKS]
dists = [s for s, frame in RAMP_MARKS]

# best a for s = 1/2 a t^2 through all the points (least squares through the origin, Chapter 171)
top = sum(s * t ** 2 for s, t in zip(dists, times))
bottom = sum(t ** 4 for t in times)
a = 2 * top / bottom
print(f"measured acceleration down the ramp: a = {a:.3f} m/s^2")

print("  s (m)   t (s)   1/2 a t^2 (m)   difference (cm)")
for s, t in zip(dists, times):
    fit = 0.5 * a * t ** 2
    print(f"  {s:4.1f}   {t:5.3f}   {fit:12.3f}   {100 * (s - fit):+12.1f}")

t_end = times[-1]
print(f"reaches the bottom (1.2 m) after {t_end:.3f} s; speed there from v = a t: {a * t_end:.2f} m/s")
print(f"average speed over the last 0.2 m: {0.2 / (times[-1] - times[-3]):.2f} m/s")
