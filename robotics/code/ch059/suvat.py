# suvat.py - the four equations of motion for constant acceleration, checked against a step-by-step sum
import math


def final_velocity(u, a, t):
    return u + a * t                        # v = u + a t


def displacement(u, a, t):
    return u * t + 0.5 * a * t ** 2         # s = u t + 1/2 a t^2


def velocity_after_distance(u, a, s):
    v_squared = u ** 2 + 2 * a * s          # v^2 = u^2 + 2 a s
    if v_squared < 0:
        return None                         # it stops before covering s
    return math.sqrt(v_squared)


u, a, t = 0.4, 0.5, 4.0                     # start at 0.4 m/s, speed up at 0.5 m/s^2 for 4 s
v = final_velocity(u, a, t)
s = displacement(u, a, t)
print(f"v = u + a t            = {v:.3f} m/s")
print(f"s = u t + 1/2 a t^2    = {s:.3f} m")
print(f"s = (u + v) / 2 x t    = {(u + v) / 2 * t:.3f} m")
print(f"v from v^2 = u^2 + 2as = {velocity_after_distance(u, a, s):.3f} m/s")

dt = 0.001
x, vel = 0.0, u
for step in range(round(t / dt)):
    x = x + (vel + 0.5 * a * dt) * dt       # area of one thin strip: its average height times its width
    vel = vel + a * dt
print(f"step-by-step sum with dt = {dt}: s = {x:.3f} m, v = {vel:.3f} m/s")
