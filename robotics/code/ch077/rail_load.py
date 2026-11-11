# rail_load.py - everything on Rover's 5 V rail is in parallel: the currents add up
RAIL_V = 5.0
REGULATOR_LIMIT_A = 1.0            # what the 5 V regulator can give

loads = [
    # name, how many, current each in A
    ("Arduino", 1, 0.050),
    ("status LEDs (with 150 ohm resistors)", 4, 0.020),
    ("line sensor", 1, 0.030),
    ("distance sensor", 1, 0.016),
    ("bumper pull-up resistors (10 kohm, when pressed)", 2, 0.0005),
    ("small servo, idle", 1, 0.010),
]
total = 0.0
print(f"{'load':50s} {'each':>8s} {'total':>8s}")
for name, n, each in loads:
    total += n * each
    print(f"{n} x {name:46s} {each * 1000:6.1f} mA {n * each * 1000:6.1f} mA")
print(f"{'rail total':50s} {'':8s} {total * 1000:6.1f} mA  = {total / REGULATOR_LIMIT_A:.0%} of the regulator")
print(f"the whole rail looks like one resistor of {RAIL_V / total:.1f} ohm")

print()
# stage 7: add a Raspberry Pi and a camera
pi = 0.800
print(f"adding a Raspberry Pi (800 mA): {(total + pi) * 1000:.0f} mA = {(total + pi) / REGULATOR_LIMIT_A:.0%} of a 1 A regulator")
print("too much: the Pi needs its own regulator (Chapter 90)")

print()
# four LEDs sharing ONE resistor instead of one each
v_led = 2.0
r_shared = (RAIL_V - v_led) / 0.080          # chosen so four LEDs get 80 mA together
print(f"four LEDs on one shared {r_shared:.1f} ohm resistor: 80 mA total, 20 mA each only if all four are identical")
print("if one LED needs 1.9 V and the others 2.0 V, it hogs most of the current: give each LED its own resistor")
