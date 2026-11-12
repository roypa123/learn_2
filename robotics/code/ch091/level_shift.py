# level_shift.py - connecting a 5 V Arduino Uno to a 3.3 V sensor board, both ways
V5, V33 = 5.0, 3.3
ABS_MAX_33 = 3.6                 # the 3.3 V chip's absolute maximum input
V_IH_33 = 2.5                    # the 3.3 V chip reads HIGH above this
V_IH_UNO = 3.0                   # the Uno reads HIGH above this
V_OH_33 = 2.9                    # a 3.3 V output's lowest guaranteed HIGH

# direction 1: Uno output -> 3.3 V input, through a divider (Chapter 79)
R_TOP, R_BOTTOM = 1000.0, 2000.0
v_out = V5 * R_BOTTOM / (R_TOP + R_BOTTOM)
i_div = V5 / (R_TOP + R_BOTTOM)
print("Uno -> 3.3 V chip, divider 1 k over 2 k:")
print(f"  HIGH arrives as {v_out:.2f} V   (needs >= {V_IH_33} V, must stay <= {ABS_MAX_33} V): "
      f"{'ok' if V_IH_33 <= v_out <= ABS_MAX_33 else 'NOT ok'}")
print(f"  the divider wastes {i_div * 1000:.2f} mA while the pin is HIGH")
r_th = R_TOP * R_BOTTOM / (R_TOP + R_BOTTOM)               # what the input "sees" (Chapter 79)
c_in = 10e-12                                              # about 10 pF of pin and wire capacitance
print(f"  edge time constant {r_th:.0f} ohm x 10 pF = {r_th * c_in * 1e9:.1f} ns: fast enough for SPI at several MHz")
print()

# direction 2: 3.3 V output -> Uno input
print("3.3 V chip -> Uno, wired directly:")
print(f"  HIGH may be only {V_OH_33} V, the Uno needs {V_IH_UNO} V: margin {V_OH_33 - V_IH_UNO:+.1f} V -> not guaranteed")
print()

# both ways: BSS138 MOSFET shifter with 10 k pull-ups
R_PULL = 10e3
C_BUS = 50e-12                                             # a short I2C bus: about 50 pF
tau = R_PULL * C_BUS
rise = 0.85 * tau                                          # time to rise from 30% to 70% of 5 V: ln(0.7/0.3) = 0.85
print("BSS138 shifter, 10 k pull-up to 5 V on the Uno side:")
print(f"  HIGH on the Uno side: {V5:.1f} V (the pull-up), margin {V5 - V_IH_UNO:+.1f} V")
print(f"  rise time 30%->70%: {rise * 1e6:.2f} us; one bit at 100 kHz I2C lasts 10 us -> ok")
print(f"  at 400 kHz (2.5 us bits) it uses {rise / 2.5e-6 * 100:.0f}% of a bit: use 4.7 k pull-ups or a shorter bus")
