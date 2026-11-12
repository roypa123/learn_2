# pi_power.py - powering Rover's Raspberry Pi (5 V, 0.8 A typical, 3 A peak): linear or switching regulator?
V_BATT = 7.2
V_OUT = 5.0
BATTERY_WH = 14.4 * 0.8           # Rover's usable energy (Chapter 5)
OTHER_W = 3.78                    # everything else on Rover (Chapter 5)

for name, i_out in [("typical", 0.8), ("peak", 3.0)]:
    p_out = V_OUT * i_out
    lin_in = V_BATT * i_out                        # a linear regulator: the same current flows in as out
    lin_heat = lin_in - p_out
    buck_in = p_out / 0.90                         # a buck converter at 90% efficiency: the same POWER in (less 10%)
    print(f"{name}: Pi takes {p_out:.1f} W")
    print(f"  linear: battery gives {lin_in:.2f} W ({lin_in / V_BATT:.2f} A), {lin_heat:.2f} W of heat, {p_out / lin_in:.0%} efficient")
    print(f"  buck  : battery gives {buck_in:.2f} W ({buck_in / V_BATT:.2f} A), {buck_in - p_out:.2f} W of heat, 90% efficient")
print()
lin_total = OTHER_W + V_BATT * 0.8
buck_total = OTHER_W + V_OUT * 0.8 / 0.9
print(f"Rover at stage 7 with the linear regulator: {lin_total:.2f} W -> {BATTERY_WH / lin_total * 60:.0f} min")
print(f"Rover at stage 7 with the buck converter:   {buck_total:.2f} W -> {BATTERY_WH / buck_total * 60:.0f} min")
