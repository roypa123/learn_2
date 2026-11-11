# arm_torque.py - how much torque must a shoulder motor give to hold a robot arm still?
import math

G = 9.81
ARM_LENGTH_M = 0.50       # shoulder to gripper
ARM_MASS_KG = 0.40        # spread evenly along the arm, so it acts at the middle
PAYLOAD_KG = 0.25         # the part in the gripper
MOTOR_MAX_NM = 3.0        # the shoulder motor after its gearbox


def holding_torque(angle_deg):
    """Torque to hold the arm still at an angle above the horizontal."""
    lever = math.cos(math.radians(angle_deg))     # horizontal distance shrinks as the arm lifts
    arm_part = ARM_MASS_KG * G * (ARM_LENGTH_M / 2) * lever
    payload_part = PAYLOAD_KG * G * ARM_LENGTH_M * lever
    return arm_part + payload_part


print(" angle   holding torque   share of the motor")
for angle in [0, 30, 60, 90, -45]:
    t = holding_torque(angle)
    print(f"{angle:5d}   {t:10.3f} N m   {t / MOTOR_MAX_NM:12.0%}")

spare = MOTOR_MAX_NM - holding_torque(0)
heaviest = (MOTOR_MAX_NM - ARM_MASS_KG * G * ARM_LENGTH_M / 2) / (G * ARM_LENGTH_M)
print(f"straight out, the motor has {spare:.3f} N m spare")
print(f"heaviest payload it can hold straight out: {heaviest:.3f} kg")
