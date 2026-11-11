# ramp_force.py - how hard must a robot push to climb a ramp?
import math

MASS_KG = 25.0
G = 9.81
WHEEL_RADIUS_M = 0.08
MOTOR_LIMIT_NM = 2.2          # both drive wheels together, after the gearbox

weight = MASS_KG * G
print(f"weight: {weight:.1f} N")
print(" slope   angle   pull down the ramp   torque needed   ok?")
for percent in [0, 5, 8.33, 10, 15]:
    angle = math.atan(percent / 100)
    along = weight * math.sin(angle)
    torque = along * WHEEL_RADIUS_M
    ok = "yes" if torque <= MOTOR_LIMIT_NM else "NO"
    print(f"{percent:5.2f}% {math.degrees(angle):6.2f} {along:15.1f} N {torque:13.2f} N m   {ok}")
