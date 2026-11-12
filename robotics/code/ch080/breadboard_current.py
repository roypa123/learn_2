# breadboard_current.py - why motors do not belong on a breadboard: contact resistance and heat
CONTACT_OHM = 0.015         # each spring contact on a typical breadboard (it varies: 0.005 to 0.05)
JUMPER_OHM = 0.10           # one 20 cm jumper wire of AWG 24 with its two pins
CONTACTS_IN_PATH = 4        # out and back, two contacts each way
JUMPERS_IN_PATH = 2
RATED_A = 1.0               # what most breadboards are rated for

r_path = CONTACTS_IN_PATH * CONTACT_OHM + JUMPERS_IN_PATH * JUMPER_OHM
print(f"resistance of the path through the breadboard: {r_path:.3f} ohm")
print(f"{'current':>8s} {'lost volts':>11s} {'heat in one contact':>20s} {'ok?':>5s}")
for amps in [0.02, 0.1, 0.5, 1.0, 1.5, 3.0]:
    lost = amps * r_path
    contact_heat = amps ** 2 * CONTACT_OHM
    ok = "yes" if amps <= RATED_A else "NO"
    print(f"{amps:6.2f} A {lost:9.3f} V {contact_heat * 1000:15.1f} mW {ok:>7s}")

print()
print("an LED (20 mA) or a sensor loses under 0.01 V: fine.")
print("Rover's motors starting at 3.1 A would lose", f"{3.1 * r_path:.2f} V", "and heat each contact by",
      f"{3.1 ** 2 * CONTACT_OHM * 1000:.0f} mW: wire motors with screw terminals or soldered joints (Chapter 92).")
