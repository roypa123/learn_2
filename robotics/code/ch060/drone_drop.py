# drone_drop.py - where must a moving drone release a parcel so it lands on the target?
import math

G = 9.81
HEIGHT_M = 20.0                 # the drone flies level at this height
SPEED = 8.0                     # m/s, flying east
TARGET_EAST_M = 100.0           # the landing pad is 100 m east of the start

fall_time = math.sqrt(2 * HEIGHT_M / G)          # s = 1/2 g t^2, so t = sqrt(2 s / g)
ahead_m = SPEED * fall_time                       # the parcel keeps the drone's sideways speed
release_east_m = TARGET_EAST_M - ahead_m
hit_speed = math.hypot(SPEED, G * fall_time)      # sideways part and downward part at the ground
hit_angle = math.degrees(math.atan2(G * fall_time, SPEED))

print(f"fall time {fall_time:.3f} s")
print(f"the parcel travels {ahead_m:.2f} m east while it falls")
print(f"release at {release_east_m:.2f} m east, {ahead_m:.2f} m before the target")
print(f"it hits the ground at {hit_speed:.1f} m/s, {hit_angle:.0f} deg below the horizontal")

dt = 0.25
x, y, vy = release_east_m, HEIGHT_M, 0.0
print("  t (s)   east (m)   height (m)")
t = 0.0
while y > 0:
    print(f"{t:6.2f}   {x:8.2f}   {y:8.2f}")
    t = t + dt
    x = release_east_m + SPEED * t
    y = HEIGHT_M - 0.5 * G * t ** 2
print(f"{fall_time:6.2f}   {TARGET_EAST_M:8.2f}   {0.0:8.2f}   <- lands")
