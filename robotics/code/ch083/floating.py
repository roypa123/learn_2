# floating.py - an input pin connected to nothing reads at random; a pull-up resistor fixes it
import random

random.seed(4)
LOW_MAX, HIGH_MIN = 1.5, 3.0          # an Uno reads below 1.5 V as LOW and above 3.0 V as HIGH (Chapter 91)
PIN_OHM = 100e6                       # an input pin is a huge resistance: about 100 Mohm


def read(volts):
    if volts <= LOW_MAX:
        return "0"
    if volts >= HIGH_MIN:
        return "1"
    return random.choice("01")         # in between, the pin may read either way


def floating_voltage(t):
    """With nothing connected, the pin's voltage drifts with whatever it picks up: mains hum, your hand, nearby wires."""
    return 2.5 + 2.4 * random.uniform(-1, 1)


def pulled_up_voltage(pickup_ua, r_pull):
    """With a pull-up to 5 V, a picked-up current of a few microamps moves the pin by only I x R."""
    return 5.0 - pickup_ua * 1e-6 * r_pull


print("20 readings, button NOT pressed:")
print("  floating      :", "".join(read(floating_voltage(t)) for t in range(20)))
for r in [10e3, 100e3, 1e6]:
    readings = "".join(read(pulled_up_voltage(random.uniform(0, 2), r)) for t in range(20))
    print(f"  pull-up {r / 1000:5.0f} k :", readings, f"(worst pin voltage {pulled_up_voltage(2, r):.2f} V)")
