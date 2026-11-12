# back_emf.py - a spinning motor is also a generator: its 'back voltage' grows with speed and cuts the current
import math

V_SUPPLY = 7.2
R = 4.8                      # winding resistance: 7.2 V / 1.5 A stall (Chapter 75)
FREE_RPM = 12000             # Rover's motor with no load (Chapter 68)
I_FREE = 0.10                # current at free speed: just enough to overcome friction inside the motor

free_rad_s = FREE_RPM * 2 * math.pi / 60
K = (V_SUPPLY - I_FREE * R) / free_rad_s        # volts of back voltage per rad/s of speed
print(f"motor constant K = {K * 1000:.3f} mV per rad/s  ({K * 1000 * 2 * math.pi / 60:.3f} mV per rpm)")
print()
print(f"{'speed (rpm)':>12s} {'back voltage':>13s} {'left for R':>11s} {'current':>9s}")
for rpm in [0, 3000, 6000, 9000, 12000]:
    w = rpm * 2 * math.pi / 60
    back = K * w
    current = (V_SUPPLY - back) / R               # Ohm's law on what is left for the winding
    print(f"{rpm:12d} {back:11.2f} V {V_SUPPLY - back:9.2f} V {current:7.3f} A")
print()
print("pushed by hand (or rolling downhill) faster than free speed, the motor makes MORE than 7.2 V:")
for rpm in [12000, 15000, 18000]:
    w = rpm * 2 * math.pi / 60
    back = K * w
    print(f"  {rpm} rpm: back voltage {back:.2f} V -> current {(V_SUPPLY - back) / R:+.3f} A (negative = flowing back INTO the battery)")
