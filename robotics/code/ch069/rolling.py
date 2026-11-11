# rolling.py - points on a rolling wheel: the bottom is still, the centre moves at v, the top at 2v
import math

R = 0.05            # wheel radius in m
V = 0.5             # robot speed in m/s
omega = V / R       # rolling without slipping: v = omega r

print(f"omega = {omega:.1f} rad/s")
for name, angle_deg in [("bottom", 270), ("front", 0), ("top", 90), ("back", 180)]:
    a = math.radians(angle_deg)
    # velocity of a rim point = velocity of the centre + velocity from turning (clockwise, so -omega)
    vx = V + (-omega) * (-R * math.sin(a))
    vy = round((-omega) * (R * math.cos(a)), 9) + 0.0      # round away a tiny -0.0
    print(f"{name:6s} of the rim: velocity ({vx:+.2f}, {vy:+.2f}) m/s, speed {math.hypot(vx, vy):.3f} m/s")

print("path of one point on the rim (a cycloid), every quarter turn:")
for k in range(0, 9):
    t = k * (math.pi / 2) / omega
    x = V * t - R * math.sin(omega * t)
    y = R - R * math.cos(omega * t)
    print(f"  t = {t:.3f} s: x = {x:.4f} m, y = {y:.4f} m")
