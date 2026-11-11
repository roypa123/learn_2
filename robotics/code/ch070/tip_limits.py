# tip_limits.py - a tall delivery robot: when does it tip on a slope, when braking, and in a corner?
import math

G = 9.81
COM_HEIGHT = 0.70        # m above the floor, with a full tray of cups
HALF_TRACK = 0.20        # m from the middle to each side wheel
COM_TO_FRONT = 0.18      # m from the centre of mass forward to the front wheels' contact line
MU_FLOOR = 0.6

# 1) standing on a side slope: tips when the weight's line passes outside the wheels
tip_side = math.degrees(math.atan(HALF_TRACK / COM_HEIGHT))
slide = math.degrees(math.atan(MU_FLOOR))
print(f"side slope: tips over at {tip_side:.1f} deg, slides at {slide:.1f} deg -> {'tips first' if tip_side < slide else 'slides first'}")

# 2) braking: tips forward when a > g x (distance to the front wheels) / height
a_tip_brake = G * COM_TO_FRONT / COM_HEIGHT
print(f"braking: tips forward above {a_tip_brake:.2f} m/s^2 (wheels slide above {MU_FLOOR * G:.2f} m/s^2)")

# 3) cornering: tips outwards when v^2 / r > g x half_track / height
a_tip_side = G * HALF_TRACK / COM_HEIGHT
for r in [0.5, 1.0, 2.0]:
    v_tip = math.sqrt(a_tip_side * r)
    v_slide = math.sqrt(MU_FLOOR * G * r)
    print(f"corner radius {r} m: tips over above {v_tip:.2f} m/s, slides above {v_slide:.2f} m/s")
