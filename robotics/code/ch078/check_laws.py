# check_laws.py - check both of Kirchhoff's laws on the mixed circuit of Chapter 77
V = 12.0
R1, R2, R3, R4 = 100.0, 200.0, 300.0, 50.0

r23 = 1 / (1 / R2 + 1 / R3)
i = V / (R1 + r23 + R4)
v_a = V - i * R1               # node A: after R1, the top of the R2/R3 pair
v_b = i * R4                   # node B: the bottom of the pair, above R4
i2 = (v_a - v_b) / R2
i3 = (v_a - v_b) / R3

print("node voltages above ground:")
print(f"  battery + : {V:6.3f} V")
print(f"  node A    : {v_a:6.3f} V")
print(f"  node B    : {v_b:6.3f} V")
print()
print("current law at node A: what flows in = what flows out")
print(f"  in  (through R1)      = {i * 1000:7.3f} mA")
print(f"  out (through R2 + R3) = {i2 * 1000:7.3f} + {i3 * 1000:7.3f} = {(i2 + i3) * 1000:7.3f} mA")
print(f"  in - out = {(i - i2 - i3) * 1000:+.6f} mA")
print()
print("voltage law round the loop battery -> R1 -> R2 -> R4 -> battery (rises +, drops -):")
terms = [("battery", +V), ("R1", -i * R1), ("R2", -i2 * R2), ("R4", -i * R4)]
for name, v in terms:
    print(f"  {name:8s} {v:+8.3f} V")
print(f"  sum      {sum(t for _, t in terms):+8.3f} V")
print()
print("voltage law round the small loop R2 -> back up through R3:")
print(f"  -{i2 * R2:.3f} + {i3 * R3:.3f} = {-i2 * R2 + i3 * R3:+.3f} V")
