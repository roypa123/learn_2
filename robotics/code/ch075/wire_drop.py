# wire_drop.py - how much voltage is lost along a wire? V_lost = I x R_wire
RHO_COPPER = 1.68e-8


def wire_ohms(length_m, area_mm2):
    return RHO_COPPER * length_m / (area_mm2 * 1e-6)


print("Rover: battery to motor driver, 0.3 m out + 0.3 m back of 0.5 mm2")
r = wire_ohms(0.6, 0.5)
for name, amps in [("idle", 0.1), ("driving", 0.53), ("motors starting", 3.1)]:
    lost = amps * r
    print(f"  {name:16s} {amps:4.2f} A: loses {lost * 1000:5.1f} mV of 7.2 V ({lost / 7.2:.2%})")

print()
print("a factory robot on a 20 m cable (40 m of wire), 48 V, drawing 5 A:")
for area in [1.5, 2.5, 4.0]:
    r = wire_ohms(40.0, area)
    lost = 5.0 * r
    print(f"  {area:3.1f} mm2: {r:5.3f} ohms, loses {lost:4.2f} V, the robot gets {48 - lost:5.2f} V")

print()
print("a cheap thin 0.2 mm2 lead on a 12 V battery, 2 m there and back, 10 A:")
r = wire_ohms(4.0, 0.2)
print(f"  {r:5.3f} ohms, loses {10 * r:4.2f} V: the motor sees only {12 - 10 * r:4.1f} V")
