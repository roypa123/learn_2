# arm_swing.py - how quickly can a shoulder motor swing an arm through 90 degrees in a flat plane?
import math

ARM_LENGTH_M = 0.50
ARM_MASS_KG = 0.40
MOTOR_MAX_NM = 3.0
SPEED_LIMIT = 6.0                  # rad/s, the joint's top speed


def arm_inertia(payload_kg, payload_at_m):
    rod = ARM_MASS_KG * ARM_LENGTH_M ** 2 / 3          # the arm itself, turning about one end
    return rod + payload_kg * payload_at_m ** 2         # plus the payload as a point mass


def swing_time(inertia, angle=math.pi / 2):
    alpha = MOTOR_MAX_NM / inertia                      # tau = I alpha, all the torque used to swing
    ramp = SPEED_LIMIT ** 2 / alpha                     # speeding up plus slowing down (Chapter 59 in angles)
    if angle >= ramp:
        return 2 * SPEED_LIMIT / alpha + (angle - ramp) / SPEED_LIMIT, alpha
    return 2 * math.sqrt(angle / alpha), alpha


print(" payload         I (kg m^2)   alpha (rad/s^2)   90 deg swing")
for kg, at in [(0.0, 0.5), (0.25, 0.5), (0.5, 0.5), (0.5, 0.25)]:
    i = arm_inertia(kg, at)
    t, a = swing_time(i)
    print(f"{kg:4.2f} kg at {at:.2f} m   {i:9.4f}   {a:12.1f}   {t:10.3f} s")
