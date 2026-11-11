# wire_resistance.py - the resistance of a wire: R = rho x length / area
RHO = {"copper": 1.68e-8, "aluminium": 2.65e-8, "iron": 9.7e-8, "nichrome": 1.1e-6}   # ohm metres


def resistance(material, length_m, area_mm2):
    """Resistance in ohms of a wire of this material, length and cross-section area."""
    return RHO[material] * length_m / (area_mm2 * 1e-6)


print("1 m of copper wire:")
for area in [0.25, 0.5, 1.0, 2.0, 4.0]:
    print(f"  {area:4.2f} mm2: {resistance('copper', 1.0, area) * 1000:7.2f} milliohms")

print()
print("Rover's battery wire, 0.3 m of 0.5 mm2:")
for material in ["copper", "aluminium", "iron"]:
    print(f"  {material:10s} {resistance(material, 0.3, 0.5) * 1000:7.2f} milliohms")

print()
print("a 20 m cable to a factory robot (there and back = 40 m):")
for area in [1.5, 2.5, 4.0]:
    print(f"  {area:3.1f} mm2 copper: {resistance('copper', 40.0, area):6.3f} ohms")

print()
r_heater = resistance("nichrome", 2.0, 0.05)
print(f"2 m of thin nichrome heater wire (0.05 mm2): {r_heater:.1f} ohms")
