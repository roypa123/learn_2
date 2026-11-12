# buck_sim.py - simulate a buck converter: a MOSFET, a diode, an inductor and a capacitor make 5 V from 8.4 V
V_IN = 8.4
V_TARGET = 5.0
L = 22e-6                  # inductor, henries
C = 100e-6                 # output capacitor, farads
R_LOAD = 2.5               # a 2 A load at 5 V
F_SW = 200_000             # switching 200,000 times a second
V_DIODE = 0.4              # Schottky diode (Chapter 86)
DT = 20e-9                 # 20 ns steps: 250 steps per switching cycle

duty = (V_TARGET + V_DIODE) / (V_IN + V_DIODE)    # the fraction of each cycle the MOSFET is on
period = 1 / F_SW
i_l, v_out, t = 0.0, 0.0, 0.0
samples = []
while t < 0.008:                                  # 8 ms: long enough for the start-up wobble to die away
    switch_on = (t % period) < duty * period
    v_node = V_IN if switch_on else -V_DIODE      # MOSFET on: the inductor sees V_IN; off: the diode carries the current
    if not switch_on and i_l <= 0:
        v_node = v_out                            # the inductor current has reached zero: nothing flows
    i_l = max(i_l + (v_node - v_out) / L * DT, 0.0)          # V = L dI/dt (Chapter 85)
    v_out = v_out + (i_l - v_out / R_LOAD) / C * DT         # I = C dV/dt (Chapter 84)
    t += DT
    if t > 0.0075:
        samples.append((v_out, i_l))

vs = [s[0] for s in samples]
ils = [s[1] for s in samples]
print(f"duty cycle {duty:.3f}: the MOSFET is on {duty * period * 1e6:.2f} us of every {period * 1e6:.1f} us")
print(f"output: average {sum(vs) / len(vs):.3f} V, ripple {(max(vs) - min(vs)) * 1000:.1f} mV peak to peak")
print(f"inductor current: average {sum(ils) / len(ils):.2f} A, from {min(ils):.2f} to {max(ils):.2f} A")
p_out = (sum(vs) / len(vs)) ** 2 / R_LOAD
print(f"load power {p_out:.2f} W; input current only while the MOSFET is on: average {sum(ils) / len(ils) * duty:.2f} A from 8.4 V")
