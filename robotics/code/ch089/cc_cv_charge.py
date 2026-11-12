# cc_cv_charge.py - how a charger fills a lithium cell: constant current, then constant voltage
from lipo_model import ocv

CAPACITY_AH = 5.0
R_CELL = 0.040              # charging path: the cell, its wires, the connector and the charger's leads
I_CHARGE = 5.0              # 1C
V_MAX = 4.20                # never above this
I_STOP = CAPACITY_AH / 20   # finish when the current has fallen to C/20 (0.25 A)
DT = 1.0                    # seconds

soc, t, phase = 0.10, 0.0, "CC"
log = []
while True:
    if phase == "CC":
        i = I_CHARGE
        if ocv(soc) + i * R_CELL >= V_MAX:      # the terminal voltage has reached 4.2 V: switch to constant voltage
            phase = "CV"
    if phase == "CV":
        i = (V_MAX - ocv(soc)) / R_CELL         # hold 4.2 V: the current is whatever that voltage pushes through
        if i <= I_STOP:
            break
    soc = min(soc + i * DT / 3600 / CAPACITY_AH, 1.0)
    t += DT
    if int(t) % 300 == 0:
        log.append((t / 60, phase, i, ocv(soc) + i * R_CELL, soc))

for minutes, ph, i, v, s in log:
    print(f"{minutes:5.0f} min  {ph}  current {i:4.2f} A  terminal {v:.3f} V  charge {s:5.1%}")
print(f"finished after {t / 60:.0f} min at {soc:.1%}")
