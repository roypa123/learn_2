# thermistor_reader.py - read a motor driver's temperature: thermistor + fixed resistor + 10-bit ADC
import math

R_25, B = 10000.0, 3950.0       # the thermistor of Chapter 74
R_FIXED = 10000.0               # on top, from 5 V
V_IN = 5.0
STEPS = 1024                    # Arduino Uno's 10-bit ADC


def thermistor(temp_c):
    return R_25 * math.exp(B * (1 / (temp_c + 273.15) - 1 / 298.15))


def count_at(temp_c):
    """The ADC count the Arduino would read at this temperature (thermistor to ground)."""
    v = V_IN * thermistor(temp_c) / (R_FIXED + thermistor(temp_c))
    return round(v / V_IN * (STEPS - 1))


def temperature_from_count(count):
    """Turn the count back into a temperature: divider formula reversed, then Chapter 74's formula reversed."""
    ratio = count / (STEPS - 1)                     # Vout / Vin
    r_therm = R_FIXED * ratio / (1 - ratio)         # from Vout/Vin = Rt / (Rf + Rt)
    inv_t = 1 / 298.15 + math.log(r_therm / R_25) / B
    return 1 / inv_t - 273.15


print(f"{'temp':>6s} {'thermistor':>11s} {'count':>6s} {'read back':>10s} {'1 count =':>10s}")
for t in [0, 25, 50, 70, 85, 100]:
    c = count_at(t)
    per_count = abs(temperature_from_count(c + 1) - temperature_from_count(c))
    print(f"{t:4d} C {thermistor(t):9.0f} ohm {c:6d} {temperature_from_count(c):8.1f} C {per_count:8.2f} C")
