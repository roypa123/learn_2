# bjt_model.py - a simple NPN transistor switching a 12 V lamp: off, half-on, and fully on (saturated)
V_CC = 12.0
R_LOAD = 40.0              # a 12 V, 0.3 A lamp (taken as a 40 ohm resistor)
BETA = 100                 # current gain: collector current = 100 x base current (when not saturated)
V_CE_SAT = 0.2             # the smallest voltage left across a fully-on transistor


def collector(ib):
    """Collector current and the voltage across the transistor, for a base current ib."""
    ic_max = (V_CC - V_CE_SAT) / R_LOAD          # the most the load lets through
    ic = min(BETA * ib, ic_max)                  # the transistor wants beta x ib, but the load sets a ceiling
    vce = V_CC - ic * R_LOAD
    return ic, vce


print(f"lamp alone on 12 V would draw {V_CC / R_LOAD * 1000:.0f} mA")
print(f"{'base current':>13s} {'collector':>10s} {'across transistor':>18s} {'heat in transistor':>19s}  state")
for ib_ma in [0.0, 0.5, 1.0, 2.0, 2.95, 5.0, 15.0]:
    ic, vce = collector(ib_ma / 1000)
    p = ic * vce
    state = "OFF" if ic == 0 else ("SATURATED (fully on)" if vce <= V_CE_SAT + 1e-9 else "half on: DANGER")
    print(f"{ib_ma:10.2f} mA {ic * 1000:7.0f} mA {vce:15.2f} V {p * 1000:15.0f} mW  {state}")
