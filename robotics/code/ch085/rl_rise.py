# rl_rise.py - the current in a coil cannot jump: it rises with the time constant L / R
import math

V = 5.0
R = 70.0              # a small 5 V relay's coil resistance, ohms
L = 0.15              # its inductance, henries
TAU = L / R
DT = TAU / 1000

print(f"relay coil: R = {R:.0f} ohm, L = {L} H, time constant L/R = {TAU * 1000:.2f} ms, final current {V / R * 1000:.1f} mA")
i, t = 0.0, 0.0
marks = [1, 2, 3, 5]
while marks:
    v_coil = V - i * R              # the voltage law: whatever the resistance does not take, the inductance does
    i = i + v_coil / L * DT         # V = L x (rate of change of I), turned round
    t = t + DT
    if t >= marks[0] * TAU - DT / 2:
        exact = V / R * (1 - math.exp(-t / TAU))
        print(f"  after {marks[0]} L/R = {t * 1000:5.2f} ms: {i * 1000:5.1f} mA (exact {exact * 1000:5.1f} mA)")
        marks.pop(0)
print()
print("the relay needs about 50 mA to pull in, so it closes roughly", f"{-TAU * math.log(1 - 0.050 / (V / R)) * 1000:.1f} ms after switch-on")
