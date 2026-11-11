# reduce_circuit.py - a mixed circuit solved step by step: shrink it to one resistor, then expand again
V_BATTERY = 12.0
R1, R2, R3, R4 = 100.0, 200.0, 300.0, 50.0     # R1, then R2 beside R3, then R4, all in a row with the battery

# step 1: the parallel pair becomes one resistor
r23 = 1 / (1 / R2 + 1 / R3)
print(f"step 1: R2 || R3 = 1 / (1/{R2:.0f} + 1/{R3:.0f}) = {r23:.1f} ohm")

# step 2: everything is now in series
r_total = R1 + r23 + R4
print(f"step 2: R1 + R23 + R4 = {R1:.0f} + {r23:.0f} + {R4:.0f} = {r_total:.0f} ohm")

# step 3: Ohm's law for the whole loop
i_total = V_BATTERY / r_total
print(f"step 3: I = {V_BATTERY:.0f} / {r_total:.0f} = {i_total * 1000:.1f} mA flows out of the battery")

# step 4: the voltage across each series part is I x R
v1, v23, v4 = i_total * R1, i_total * r23, i_total * R4
print(f"step 4: V1 = {v1:.2f} V, V23 = {v23:.2f} V, V4 = {v4:.2f} V   (sum {v1 + v23 + v4:.2f} V = the battery)")

# step 5: inside the parallel pair, both have V23 across them; each current is V23 / R
i2, i3 = v23 / R2, v23 / R3
print(f"step 5: I2 = {v23:.2f} / {R2:.0f} = {i2 * 1000:.1f} mA, I3 = {v23:.2f} / {R3:.0f} = {i3 * 1000:.1f} mA   (sum {(i2 + i3) * 1000:.1f} mA = I)")

# bonus: power in each part, and the total
powers = [v1 * i_total, v23 * i2, v23 * i3, v4 * i_total]
print(f"powers: R1 {powers[0] * 1000:.0f} mW, R2 {powers[1] * 1000:.0f} mW, R3 {powers[2] * 1000:.0f} mW, R4 {powers[3] * 1000:.0f} mW; "
      f"total {sum(powers) * 1000:.0f} mW = battery {V_BATTERY * i_total * 1000:.0f} mW")
