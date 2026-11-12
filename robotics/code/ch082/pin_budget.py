# pin_budget.py - how many LEDs can an Arduino Uno drive straight from its pins?
PIN_HIGH_V = 4.7             # a pin's voltage when it supplies about 10 mA (it sags a little under load)
PIN_LIMIT_MA = 20            # the recommended current per pin (absolute maximum 40 mA)
CHIP_LIMIT_MA = 200          # the most the whole chip should supply from all its pins together

leds = [
    # name, forward voltage, resistor in ohms
    ("power (green)", 2.2, 1000),
    ("driving (blue)", 3.1, 470),
    ("battery low (red)", 2.0, 330),
    ("bumper left (yellow)", 2.1, 330),
    ("bumper right (yellow)", 2.1, 330),
    ("line seen (red)", 2.0, 220),
    ("obstacle (red)", 2.0, 150),
]
total = 0.0
print(f"{'LED':24s} {'R':>6s} {'current':>9s} {'per pin':>8s}")
for name, vf, r in leds:
    i = (PIN_HIGH_V - vf) / r * 1000
    total += i
    print(f"{name:24s} {r:6d} {i:7.1f} mA {'ok' if i <= PIN_LIMIT_MA else 'TOO MUCH':>8s}")
print(f"{'all LEDs on at once':24s} {'':6s} {total:7.1f} mA = {total / CHIP_LIMIT_MA:.0%} of the chip's limit")
print()
print("a modern LED is clearly visible at 2-5 mA indoors: 1 kohm from 5 V is plenty for a status light")
