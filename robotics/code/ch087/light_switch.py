# light_switch.py - a phototransistor feeds a power transistor: more light, more motor current (Moth's idea)
V = 6.0                     # Moth's battery: 4 x AA
PHOTO_UA_PER_LUX = 0.5      # the phototransistor passes about 0.5 uA for each lux falling on it
BETA = 150                  # the power transistor's gain
R_MOTOR = 15.0              # a small toy motor (taken as 15 ohm)
V_CE_SAT = 0.2
I_START = 0.08              # the motor needs about 80 mA to start turning

i_max = (V - V_CE_SAT) / R_MOTOR
print(f"motor current when fully on: {i_max * 1000:.0f} mA")
print(f"{'light (lux)':>12s} {'photo current':>14s} {'motor current':>14s}  motor")
for lux in [10, 100, 300, 600, 1000, 2000, 5000]:
    ib = lux * PHOTO_UA_PER_LUX * 1e-6         # the phototransistor's current becomes the power transistor's base current
    ic = min(BETA * ib, i_max)
    state = "stopped" if ic < I_START else ("full speed" if ic >= i_max - 1e-9 else "turning")
    print(f"{lux:12d} {ib * 1e6:11.0f} uA {ic * 1000:11.0f} mA  {state}")
print()
print(f"the motor starts at about {I_START / BETA / (PHOTO_UA_PER_LUX * 1e-6):.0f} lux and is at full speed above {i_max / BETA / (PHOTO_UA_PER_LUX * 1e-6):.0f} lux")
print()
print("one transistor needs a bright desk lamp. Two in a 'Darlington pair' multiply their gains:")
beta2 = BETA * BETA
print(f"  gain {BETA} x {BETA} = {beta2}: the motor starts at about {I_START / beta2 / (PHOTO_UA_PER_LUX * 1e-6):.1f} lux")
print("  so sensitive that ordinary room light switches it fully on: Moth (Chapter 93) compares TWO sensors instead")
