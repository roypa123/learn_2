# linear_map.py - move a value from one range to another along a straight line
def map_range(value, in_low, in_high, out_low, out_high):
    m = (out_high - out_low) / (in_high - in_low)
    return out_low + m * (value - in_low)


print("ADC reading to volts")
for raw in [0, 512, 1023]:
    print(f"  {raw:5d} -> {map_range(raw, 0, 1023, 0.0, 5.0):.3f} V")

print("joystick to speed command")
for raw in [0, 256, 512, 1023]:
    print(f"  {raw:5d} -> {map_range(raw, 0, 1023, -100, 100):+.1f} %")

print("servo angle to pulse width")
for angle in [0, 45, 90, 180]:
    print(f"  {angle:5d} -> {map_range(angle, 0, 180, 1000, 2000):.0f} us")
