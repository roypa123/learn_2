# switch_design.py - a pin cannot drive a 300 mA headlight. Design a BJT switch and a MOSFET switch for it.
V_PIN, V_BE = 5.0, 0.7
LOAD_A = 0.30                       # Rover's LED headlight: 5 V, 300 mA
PIN_SAFE_MA = 20.0

print("BJT (2N2222): the base current must be large enough to switch it fully on (Chapter 87)")
for forced_beta in [10, 20, 50]:    # how many times bigger the collector current is than the base current
    i_b = LOAD_A / forced_beta
    r_b = (V_PIN - V_BE) / i_b      # the base resistor that gives this base current
    pin_ok = "ok" if i_b * 1000 <= PIN_SAFE_MA else "TOO MUCH for the pin"
    print(f"  forced beta {forced_beta:2d}: base {i_b * 1000:5.1f} mA, base resistor {r_b:6.0f} ohm -> {pin_ok}")
v_ce_sat = 0.3                      # the BJT's voltage when fully on, at 300 mA
print(f"  heat in the BJT when on: {v_ce_sat} V x {LOAD_A} A = {v_ce_sat * LOAD_A * 1000:.0f} mW")
print()

print("Logic-level MOSFET (e.g. AO3400): the gate takes almost no steady current (Chapter 88)")
r_ds_on = 0.04                      # ohms when the gate is at 4.5 V or more
print(f"  heat in the MOSFET when on: {LOAD_A} A^2 x {r_ds_on} ohm = {LOAD_A ** 2 * r_ds_on * 1000:.1f} mW")
q_gate, r_gate = 7e-9, 220          # gate charge and a 220 ohm resistor in series with the gate
i_peak = V_PIN / r_gate
print(f"  gate resistor {r_gate} ohm: peak pin current {i_peak * 1000:.0f} mA for about "
      f"{q_gate / i_peak * 1e9:.0f} ns while the gate charges, then 0 mA")
