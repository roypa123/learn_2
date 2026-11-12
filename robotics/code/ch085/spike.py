# spike.py - switch off a coil: the current wants to keep flowing, and the voltage jumps to whatever it takes
V = 5.0
R_COIL = 70.0
L = 0.15
I0 = V / R_COIL                  # the current flowing at the moment of switch-off
SWITCH_OFF_S = 1e-6              # a transistor switches off in about a microsecond

print(f"coil current at switch-off: {I0 * 1000:.1f} mA, stored energy 1/2 L I^2 = {0.5 * L * I0 ** 2 * 1000:.3f} mJ")
print()
print("1) nothing to catch the current: the transistor tries to stop it in 1 us")
v_spike = L * I0 / SWITCH_OFF_S
print(f"   V = L x dI/dt = {L} x {I0:.4f} / {SWITCH_OFF_S} = {v_spike:,.0f} V")
print("   (in reality the transistor breaks down, or a spark jumps, long before that)")
print()
print("2) a resistor across the coil gives the current another path")
print(f"{'escape resistor':>17s} {'spike at switch':>16s} {'current dies in (5 tau)':>24s}")
for r_esc in [10_000, 1_000, 100, 10]:
    spike_at_switch = V + I0 * r_esc          # the coil pushes I0 through the escape resistor, on top of the supply
    tau = L / (R_COIL + r_esc)
    print(f"{r_esc:13d} ohm {spike_at_switch:12.1f} V {5 * tau * 1000:18.2f} ms")
print()
print("3) a diode across the coil (Chapter 86): the spike is limited to the supply + about 0.7 V")
print(f"   switch sees about {V + 0.7:.1f} V; the current dies in about {5 * L / R_COIL * 1000:.0f} ms")
