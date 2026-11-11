# power_forms.py - electrical power three ways: P = V x I = I^2 x R = V^2 / R
cases = [
    # name, volts across, amps through
    ("LED (2 V, 20 mA)", 2.0, 0.020),
    ("LED's 150 ohm resistor", 3.0, 0.020),
    ("Rover's wire at start-up", 0.031, 3.1),
    ("Rover motor, stalled", 7.2, 1.5),
    ("Rover motor, driving", 7.2, 0.25),
    ("kettle on the mains", 230.0, 8.7),
]
print(f"{'part':26s} {'V':>7s} {'I':>7s} {'R = V/I':>9s} {'V x I':>8s} {'I^2 R':>8s} {'V^2 / R':>8s}")
for name, v, i in cases:
    r = v / i
    print(f"{name:26s} {v:7.3f} {i:7.3f} {r:9.3f} {v * i:8.3f} {i * i * r:8.3f} {v * v / r:8.3f}")

print()
print("the Chapter 7 link between watts and amps:")
rover_w = 3.78
print(f"  Rover uses {rover_w} W from 7.2 V, so I = P / V = {rover_w / 7.2:.2f} A   (Chapter 7 used 0.53 A)")
print(f"  a 2,000 W kettle on 230 V draws {2000 / 230:.1f} A; on 12 V it would need {2000 / 12:.0f} A")
