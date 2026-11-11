# driver_heat.py - Rover's motor driver: how much heat, how hot, and for how long can the motors stall?
R_ON = 0.5              # ohms: the driver's own resistance in each motor's path (from the TB6612 datasheet)
THETA_BARE = 60.0       # degrees C per watt, chip to air, on its small board
THETA_SINK = 25.0       # with a small stuck-on heat sink
T_MAX = 150.0           # the chip's limit
ROOM = 25.0
HEAT_CAPACITY = 1.5     # joules per degree: how much energy warms the chip and its board by 1 degree
DT = 0.1

for name, amps in [("driving", 0.5), ("one motor stalled", 1.5), ("both motors stalled", 1.5)]:
    motors = 1 if name == "one motor stalled" else 2
    watts = motors * amps ** 2 * R_ON                   # I^2 R in each channel
    print(f"{name:20s}: {watts:5.3f} W of heat; steady rise {watts * THETA_BARE:5.1f} C bare, {watts * THETA_SINK:5.1f} C with heat sink")

print()
# both motors stalled: how long until the chip reaches 150 C? Step forward in time (Chapter 71)
watts = 2 * 1.5 ** 2 * R_ON
for theta, label in [(THETA_BARE, "bare"), (THETA_SINK, "with heat sink")]:
    temp, t = ROOM, 0.0
    while temp < T_MAX and t < 600:
        cooling = (temp - ROOM) / theta                 # watts flowing out to the air
        temp = temp + (watts - cooling) / HEAT_CAPACITY * DT
        t = t + DT
    if temp >= T_MAX:
        print(f"{label:15s}: reaches {T_MAX:.0f} C after {t:5.1f} s of stall")
    else:
        print(f"{label:15s}: settles at {temp:5.1f} C, never reaches {T_MAX:.0f} C")
