# battery_monitor.py - let a 3.3 V flight controller measure a 4S drone battery (up to 16.8 V)
ADC_MAX_V = 3.3
ADC_STEPS = 4096           # a 12-bit ADC (Chapter 101)
V_FULL = 16.8
STANDARD = [1000, 1500, 2200, 3300, 4700, 6800, 10000, 15000, 22000, 33000, 47000, 68000, 100000]

# the largest ratio allowed, with a 10% margin for spikes
max_ratio = ADC_MAX_V / V_FULL / 1.1
print(f"Vout / Vin must stay below {max_ratio:.4f}")

best = None
for r2 in STANDARD:
    for r1 in STANDARD:
        ratio = r2 / (r1 + r2)
        if ratio <= max_ratio and r1 + r2 >= 20000:          # under the limit, and not wasting much current
            if best is None or ratio > best[2]:
                best = (r1, r2, ratio)
r1, r2, ratio = best
print(f"chosen: R1 = {r1} ohm, R2 = {r2} ohm, ratio {ratio:.4f}")
print(f"full pack 16.8 V -> {16.8 * ratio:.3f} V at the ADC")
print(f"empty pack 13.2 V -> {13.2 * ratio:.3f} V at the ADC")
step_v = ADC_MAX_V / ADC_STEPS / ratio
print(f"one ADC step = {ADC_MAX_V / ADC_STEPS * 1000:.3f} mV at the ADC = {step_v * 1000:.2f} mV of battery voltage")
current = V_FULL / (r1 + r2)
print(f"the divider draws {current * 1000:.3f} mA: {current * 1000 * 24 * 30:.0f} mAh in a month of storage")
print(f"its output resistance is {r1 * r2 / (r1 + r2):.0f} ohm")

print()
print("reading back: the flight controller turns an ADC count into the battery voltage")
for count in [3000, 3500, 3700]:
    v_adc = count / ADC_STEPS * ADC_MAX_V
    v_batt = v_adc / ratio
    print(f"  count {count}: {v_adc:.3f} V at the ADC -> battery {v_batt:.2f} V = {v_batt / 4:.3f} V per cell")
