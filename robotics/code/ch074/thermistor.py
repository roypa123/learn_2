# thermistor.py - a resistor whose resistance changes with temperature, used to watch a motor driver
import math

R_25 = 10000.0        # ohms at 25 degrees C
B = 3950.0            # the thermistor's 'B value' from its datasheet
T0_K = 25 + 273.15    # 25 degrees C in kelvin


def resistance(temp_c):
    """Resistance of an NTC thermistor at a temperature in degrees C."""
    temp_k = temp_c + 273.15
    return R_25 * math.exp(B * (1 / temp_k - 1 / T0_K))


def temperature(ohms):
    """The temperature in degrees C that gives this resistance (the formula turned round)."""
    inv_t = 1 / T0_K + math.log(ohms / R_25) / B
    return 1 / inv_t - 273.15


print(f"{'temp (C)':>9s} {'resistance':>12s}")
for t in [-10, 0, 25, 50, 80, 100]:
    print(f"{t:9d} {resistance(t):10.0f} ohms")

print()
for ohms in [8000, 4000, 2000, 1000]:
    t = temperature(ohms)
    state = "OK" if t < 70 else "WARNING: slow the motors" if t < 85 else "STOP: too hot"
    print(f"measured {ohms:5d} ohms -> {t:5.1f} C  {state}")
