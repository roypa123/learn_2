# lidar_scan.py - turn a laser scan (angle and range) into points on the floor
import numpy as np

angles_deg = np.arange(0, 360, 45)          # 8 beams, 45 degrees apart
ranges_m = np.array([2.0, 1.5, 1.0, 0.8, 1.0, np.inf, 3.0, 2.5])   # inf = nothing was hit

hit = np.isfinite(ranges_m)                 # True where the beam hit something
angles_rad = np.radians(angles_deg[hit])    # the maths functions need radians
r = ranges_m[hit]

x_m = r * np.cos(angles_rad)                # one line for every beam at once
y_m = r * np.sin(angles_rad)

for px, py in zip(x_m, y_m):
    print(f"({px:6.2f}, {py:6.2f})")

nearest = r.argmin()                        # the POSITION of the smallest range
print(f"beams that hit: {hit.sum()} of {hit.size}")
print(f"nearest object: {r[nearest]} m at {angles_deg[hit][nearest]} degrees")
