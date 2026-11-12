# rover_vin.py - power Rover's Uno through VIN, or from Rover's own LDO into the 5V pin?
# Watch the 5 V rail as the battery empties, and what a sagging rail does to the battery reading.
DIODE, DROPOUT = 0.8, 1.1          # the Uno's own path from VIN: diode, then the regulator (uno_power.py)
LDO_DROPOUT = 0.3                  # Rover's low-dropout regulator (Chapter 90)
DIVIDER = 0.5                      # the battery is read on A3 through two equal resistors (Chapter 79)


def rail(v_bat, path):
    if path == "VIN":
        return min(5.0, v_bat - DIODE - DROPOUT)     # out of headroom: the rail follows the battery down
    return min(5.0, v_bat - LDO_DROPOUT)


def battery_reading(v_bat, v_ref):
    count = int(v_bat * DIVIDER / v_ref * 1024)      # the ADC compares A3 with its own 5 V rail (Chapter 91)
    return count * 5.0 / 1024 / DIVIDER              # the sketch believes the rail is exactly 5.0 V


print(f"{'battery':>8s} | {'VIN rail':>8s} {'sketch reads':>12s} | {'LDO rail':>8s} {'sketch reads':>12s}")
for v_bat in [8.4, 7.8, 7.2, 6.9, 6.6, 6.3, 6.0]:
    cols = []
    for path in ["VIN", "LDO"]:
        r = rail(v_bat, path)
        cols.append(f"{r:7.2f} V {battery_reading(v_bat, r):11.2f} V")
    warn = "  <- below 4.5 V: the chip is out of spec at 16 MHz" if rail(v_bat, "VIN") < 4.5 else ""
    print(f"{v_bat:7.1f} V | {cols[0]} | {cols[1]}{warn}")
