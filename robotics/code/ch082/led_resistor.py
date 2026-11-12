# led_resistor.py - choose the series resistor for an LED: R = (V_supply - V_forward) / I
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]       # the standard resistor values


def next_standard(r):
    """The smallest E12 value that is at least r (so the current is a little LESS than asked)."""
    decade = 1.0
    while decade * 10 <= r:
        decade *= 10
    while decade > r:
        decade /= 10
    for scale in [decade, decade * 10]:
        for v in E12:
            if v * scale >= r - 1e-9:
                return v * scale


LEDS = {"red": 2.0, "yellow": 2.1, "green": 2.2, "blue": 3.1, "white": 3.1}
print(f"{'LED':7s} {'supply':>7s} {'want':>6s} {'exact R':>8s} {'use':>7s} {'actual I':>9s} {'R power':>8s}")
for supply in [5.0, 3.3]:
    for colour, vf in LEDS.items():
        want = 0.010                                    # 10 mA: bright enough for a status light
        exact = (supply - vf) / want
        use = next_standard(exact)
        actual = (supply - vf) / use
        print(f"{colour:7s} {supply:5.1f} V {want * 1000:4.0f} mA {exact:7.0f} {use:6.0f} {actual * 1000:7.1f} mA {actual ** 2 * use * 1000:6.1f} mW")
    print()
print("a blue or white LED from 3.3 V has only 0.2 V left for the resistor: its current depends strongly on Vf")
