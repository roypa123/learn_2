# ohm.py - Ohm's law: give any two of V, I and R, and get the third
def ohm(v=None, i=None, r=None):
    """Return (v, i, r). Exactly one of them must be None; it is worked out from the other two."""
    if v is None:
        v = i * r                 # V = I x R
    elif i is None:
        i = v / r                 # I = V / R
    elif r is None:
        r = v / i                 # R = V / I
    return v, i, r


examples = [
    ("Rover motor, 3 ohms, on 7.2 V", dict(v=7.2, r=3.0)),
    ("LED resistor, 150 ohms, 3 V across it", dict(v=3.0, r=150.0)),
    ("wet hand, 1,000 ohms, on 230 V mains", dict(v=230.0, r=1000.0)),
    ("dry hand, 100,000 ohms, on Rover's 7.2 V", dict(v=7.2, r=100000.0)),
    ("Rover wire, 0.01 ohms, carrying 3.1 A", dict(i=3.1, r=0.01008)),
    ("unknown part: 5 V across, 0.025 A through", dict(v=5.0, i=0.025)),
    ("Rover motor stalled: 7.2 V, 1.5 A", dict(v=7.2, i=1.5)),
]
print(f"{'case':46s} {'V':>8s} {'I':>9s} {'R':>11s}")
for name, known in examples:
    v, i, r = ohm(**known)
    print(f"{name:46s} {v:8.3f} {i:9.4f} {r:11.3f}")
