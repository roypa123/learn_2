# switching_loss.py - one MOSFET in a drone ESC: heat from being on, plus heat from every switch-over
V_BUS = 22.2            # 6S drone pack (Chapter 74)
I_MOTOR = 30.0          # current in one phase at full throttle
R_ON = 0.002            # 2 milliohms when fully on
T_SWITCH = 50e-9        # 50 ns to go from off to on (and the same from on to off)
DUTY = 0.5              # on for half of each cycle (Chapter 102)
Q_GATE = 30e-9          # 30 nC of charge to fill the gate each time it switches on
V_GATE = 10.0

conduction = I_MOTOR ** 2 * R_ON * DUTY
print(f"conduction heat (I^2 R while on, half the time): {conduction:.2f} W")
print(f"{'PWM frequency':>14s} {'switching heat':>15s} {'total':>8s} {'gate driver current':>20s}")
for f in [8_000, 24_000, 48_000, 96_000]:
    switching = 0.5 * V_BUS * I_MOTOR * (2 * T_SWITCH) * f      # a triangle of V x I during each on and off transition
    gate_ma = Q_GATE * f * 1000
    print(f"{f / 1000:10.0f} kHz {switching:12.2f} W {conduction + switching:6.2f} W {gate_ma:15.2f} mA")
print()
print("faster PWM: smoother motor current, but more switching heat; 24 kHz is a common choice for drones")
