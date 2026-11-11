# wire_heat.py - the heat made in each metre of wire: P per metre = I^2 x rho / A
RHO = 1.68e-8


def watts_per_metre(current_a, area_mm2):
    return current_a ** 2 * RHO / (area_mm2 * 1e-6)


print("heat in watts per metre of copper wire")
areas = [0.5, 1.0, 2.0, 4.0, 6.0]
print(f"{'current':>8s}" + "".join(f"{a:>9.1f}" for a in areas) + "   mm2")
for amps in [1, 3.1, 10, 20, 40]:
    row = "".join(f"{watts_per_metre(amps, a):9.2f}" for a in areas)
    print(f"{amps:6.1f} A {row}")

print()
print("double the current, four times the heat:")
for amps in [10, 20, 40]:
    print(f"  {amps:2d} A in 1 mm2: {watts_per_metre(amps, 1.0):5.1f} W/m")
print()
print("the drone's 1 m of 4 mm2 wire at 40 A makes", f"{watts_per_metre(40, 4.0):.1f} W of heat;",
      f"1 mm2 would make {watts_per_metre(40, 1.0):.1f} W")
