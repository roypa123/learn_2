# convert.py - change a length from any unit to any other unit
TO_METRES = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
}


def convert(value, from_unit, to_unit):
    metres = value * TO_METRES[from_unit]
    return metres / TO_METRES[to_unit]


print(f"1.012 m  = {convert(1.012, 'm', 'mm'):.1f} mm")
print(f"8 in     = {convert(8, 'in', 'cm'):.2f} cm")
print(f"5280 ft  = {convert(5280, 'ft', 'km'):.4f} km")
print(f"65.89 mm = {convert(65.89, 'mm', 'in'):.3f} in")
