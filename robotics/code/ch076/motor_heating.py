# motor_heating.py - a humanoid's leg motor holding a pose: I^2 R heat, and how long before it is too hot
import math

WINDING_OHM = 0.3
HOLD_A = 20.0                  # current needed to hold the pose
HEAT_CAPACITY = 450.0          # J per degree C (about 0.5 kg of copper and iron)
THETA = 1.5                    # degrees C per watt from the winding to the air
ROOM = 20.0
LIMIT = 100.0                  # the winding insulation's safe limit
DT = 1.0

watts = HOLD_A ** 2 * WINDING_OHM
steady = ROOM + watts * THETA
tau = HEAT_CAPACITY * THETA
print(f"holding at {HOLD_A} A makes {watts:.0f} W of heat in the winding")
print(f"if it stood for ever it would settle at {steady:.0f} C (time constant {tau:.0f} s)")

temp, t = ROOM, 0.0
while temp < LIMIT:
    temp = temp + (watts - (temp - ROOM) / THETA) / HEAT_CAPACITY * DT      # Euler step (Chapter 71)
    t = t + DT
    if t % 60 == 0:
        print(f"  after {t / 60:3.0f} min: {temp:5.1f} C")
print(f"the winding reaches {LIMIT:.0f} C after {t / 60:.1f} min: the robot must sit or change pose before then")
exact = -tau * math.log(1 - (LIMIT - ROOM) / (steady - ROOM))
print(f"(the exact exponential formula gives {exact / 60:.1f} min)")
