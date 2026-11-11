# shunt.py - choosing a small 'sense' resistor that turns a motor's current into a voltage
SUPPLY = 7.2
STALL_A = 1.5              # Rover's motor when it is blocked
NORMAL_A = 0.5
ADC_STEP_V = 5.0 / 1024    # the Arduino reads 0-5 V in 1,024 steps (Chapter 101)

print(f"the Arduino sees steps of {ADC_STEP_V * 1000:.2f} mV")
print(f"{'shunt':>8s} {'at 0.5 A':>10s} {'at stall':>10s} {'lost at stall':>14s} {'amps per step':>14s}")
for r in [0.01, 0.05, 0.1, 0.5, 1.0]:
    v_normal = NORMAL_A * r                  # V = I x R
    v_stall = STALL_A * r
    lost = v_stall / SUPPLY                  # share of the motor's voltage eaten by the shunt
    per_step = ADC_STEP_V / r                # I = V / R: the smallest current change the Arduino can see
    print(f"{r:6.2f} ohm {v_normal * 1000:7.0f} mV {v_stall * 1000:7.0f} mV {lost:13.1%} {per_step:13.3f} A")

print()
print("rule: a stall must be easy to see (many ADC steps) but the shunt must eat little voltage")
chosen = 0.1
threshold_a = 1.0
print(f"with {chosen} ohm, a stall alarm at {threshold_a} A means 'voltage above {threshold_a * chosen * 1000:.0f} mV'")
print(f"that is ADC reading above {threshold_a * chosen / ADC_STEP_V:.0f}")
