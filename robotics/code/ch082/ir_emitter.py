# ir_emitter.py - the infrared LED in Rover's line sensor: choose its resistor, then check the worst case
VF_IR = 1.2                 # an infrared LED's forward voltage at 20 mA (lower than visible LEDs)
VF_SPREAD = 0.1             # the datasheet: 1.1 to 1.3 V
SUPPLY = 5.0
SUPPLY_SPREAD = 0.25        # a 5 V rail can be 4.75 to 5.25 V
WANT_MA = 20.0
MAX_MA = 50.0               # the LED's absolute maximum continuous current
E12 = [100, 120, 150, 180, 220, 270, 330]

exact = (SUPPLY - VF_IR) / (WANT_MA / 1000)
print(f"exact resistor for {WANT_MA:.0f} mA: {exact:.0f} ohm")
for r in E12:
    if r >= exact:
        chosen = r
        break
print(f"next standard value up: {chosen} ohm")

worst_high = (SUPPLY + SUPPLY_SPREAD - (VF_IR - VF_SPREAD)) / (chosen * 0.95) * 1000      # high supply, low Vf, R 5% low
worst_low = (SUPPLY - SUPPLY_SPREAD - (VF_IR + VF_SPREAD)) / (chosen * 1.05) * 1000        # low supply, high Vf, R 5% high
typical = (SUPPLY - VF_IR) / chosen * 1000
print(f"typical {typical:.1f} mA, worst case {worst_low:.1f} to {worst_high:.1f} mA (limit {MAX_MA:.0f} mA)")
power = (worst_high / 1000) ** 2 * chosen * 0.95
print(f"resistor power in the worst case {power * 1000:.0f} mW: a 1/4 W resistor is fine")

print()
print("five sensors along a line-following bar, all lit all the time:")
print(f"  {5 * typical:.0f} mA from the 5 V rail, {5 * typical / 1000 * SUPPLY:.2f} W")
print("  pulsing them only while reading (Chapter 102) cuts that by the duty cycle")
