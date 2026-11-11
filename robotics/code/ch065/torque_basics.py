# torque_basics.py - torque = force x lever arm, and balancing torques on a seesaw
import math

# pushing a door with 20 N at different distances from the hinges, at right angles
for r in [0.05, 0.40, 0.80]:
    print(f"20 N at {r:.2f} m from the hinge: torque {20 * r:5.2f} N m")

# the same 20 N at 0.80 m, but pushing at different angles to the door
for angle_deg in [90, 60, 30, 0]:
    torque = 20 * 0.80 * math.sin(math.radians(angle_deg))
    print(f"push at {angle_deg:2d} deg to the door: torque {torque:5.2f} N m")

# a seesaw: 30 kg child 1.5 m left of the pivot; where must a 45 kg child sit to balance?
G = 9.81
left_torque = 30 * G * 1.5                       # anticlockwise
right_distance = left_torque / (45 * G)          # clockwise must be equal
print(f"left child's torque {left_torque:.1f} N m, so the 45 kg child sits {right_distance:.2f} m right of the pivot")

# wheel torque and the push on the ground (Chapter 49 and Chapter 61)
WHEEL_TORQUE_NM = 2.2
for radius in [0.04, 0.08, 0.16]:
    print(f"2.2 N m on a wheel of radius {radius:.2f} m pushes with {WHEEL_TORQUE_NM / radius:5.1f} N")
