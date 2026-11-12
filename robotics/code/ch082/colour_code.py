# colour_code.py - read and write the coloured bands on a resistor
COLOURS = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white"]
MULTIPLIER = {c: 10 ** k for k, c in enumerate(COLOURS)}
MULTIPLIER.update({"gold": 0.1, "silver": 0.01})
TOLERANCE = {"brown": "1%", "red": "2%", "gold": "5%", "silver": "10%"}


def decode(bands):
    """4 bands: digit, digit, multiplier, tolerance. 5 bands: digit, digit, digit, multiplier, tolerance."""
    digits = bands[:-2]
    value = 0
    for b in digits:
        value = value * 10 + COLOURS.index(b)
    return value * MULTIPLIER[bands[-2]], TOLERANCE[bands[-1]]


def encode(ohms, bands=4, tolerance="gold"):
    """The colours for a value, e.g. 4700 -> yellow violet red gold."""
    n_digits = bands - 2
    exponent = 0
    while ohms >= 10 ** n_digits - 0.5:
        ohms /= 10
        exponent += 1
    while ohms < 10 ** (n_digits - 1) - 1e-9:
        ohms *= 10
        exponent -= 1
    digits = str(round(ohms)).zfill(n_digits)
    mult = {-1: "gold", -2: "silver"}.get(exponent, COLOURS[exponent] if exponent >= 0 else None)
    return [COLOURS[int(d)] for d in digits] + [mult, tolerance]


def pretty(ohms):
    for unit, size in [("M", 1e6), ("k", 1e3)]:
        if ohms >= size:
            return f"{ohms / size:g} {unit}ohm"
    return f"{ohms:g} ohm"


for bands in [["brown", "black", "red", "gold"], ["yellow", "violet", "red", "gold"],
              ["brown", "green", "black", "gold"], ["red", "red", "black", "brown", "brown"],
              ["blue", "grey", "gold", "gold"]]:
    value, tol = decode(bands)
    print(f"{' '.join(bands):34s} -> {pretty(value)} +/-{tol}")
print()
for ohms in [150, 220, 1000, 4700, 10000, 2.2, 100000]:
    print(f"{pretty(ohms):9s} -> {' '.join(encode(ohms))}")
