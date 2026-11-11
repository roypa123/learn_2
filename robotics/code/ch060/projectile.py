# projectile.py - a throw: the sideways part and the up-down part, worked out separately
import math

G = 9.81


def throw(speed, angle_deg, start_height, land_height=0.0):
    """Return (flight time, distance across, highest point) for a throw without air resistance."""
    ux = speed * math.cos(math.radians(angle_deg))     # sideways part: never changes
    uy = speed * math.sin(math.radians(angle_deg))     # upward part: gravity changes it
    # land when start_height + uy t - 1/2 G t^2 = land_height  (a quadratic in t, Chapter 45)
    a, b, c = -0.5 * G, uy, start_height - land_height
    disc = b * b - 4 * a * c
    if disc < 0:
        return None                                    # never comes down to that height
    t_land = (-b - math.sqrt(disc)) / (2 * a)          # the later of the two roots
    highest = start_height + uy ** 2 / (2 * G)          # v^2 = u^2 + 2 a s at the top, where vy = 0
    return t_land, ux * t_land, highest


if __name__ == "__main__":
    speed = math.hypot(2.4, 4.0)                       # the Chapter 45 throw: 2.4 m/s across, 4.0 m/s up
    angle = math.degrees(math.atan2(4.0, 2.4))
    t, x, top = throw(speed, angle, 0.5, land_height=0.3)
    print(f"speed {speed:.3f} m/s at {angle:.2f} deg")
    print(f"Chapter 45 parcel: lands at bin height after {t:.3f} s, {x:.3f} m away, highest point {top:.3f} m")

    print("angle   time    range   highest   (5 m/s, thrown from the ground)")
    for angle in [15, 30, 45, 60, 75]:
        t, x, top = throw(5.0, angle, 0.0)
        print(f"{angle:4d}   {t:5.3f}  {x:6.3f}   {top:6.3f}")
