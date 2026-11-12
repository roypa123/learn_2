# stripboard_check.py - check a stripboard layout before you solder: which holes are really connected?
# The board has copper strips running left to right along each row. A cut at (row, col) breaks the strip there.

PARTS = {
    # part: {pin: (row, col)}
    "J1 (to Uno)": {"5V": (0, 0), "TX": (1, 0), "GND": (2, 0)},
    "J2 (to Pi)": {"GND": (2, 9), "RX": (3, 9)},
    "R1 1k": {"a": (1, 2), "b": (3, 2)},
    "R2 2k": {"a": (3, 4), "b": (2, 4)},
    "R3 330": {"a": (0, 7), "b": (1, 7)},
    "LED1": {"anode": (1, 8), "cathode": (2, 8)},
}
WANTED = {
    "5V": {"J1 (to Uno).5V", "R3 330.a"},
    "UNO_TX": {"J1 (to Uno).TX", "R1 1k.a"},
    "PI_RX": {"R1 1k.b", "R2 2k.a", "J2 (to Pi).RX"},
    "GND": {"J1 (to Uno).GND", "R2 2k.b", "LED1.cathode", "J2 (to Pi).GND"},
    "LED_A": {"R3 330.b", "LED1.anode"},
}


def strip_piece(row, col, cuts):
    """Name the piece of copper a hole sits on: its row, and how many cuts lie to its left."""
    if (row, col) in cuts:
        return None                                   # the hole itself was drilled away
    return (row, sum(1 for (r, c) in cuts if r == row and c < col))


def check(cuts):
    pieces = {}
    for part, pins in PARTS.items():
        for pin, (row, col) in pins.items():
            piece = strip_piece(row, col, cuts)
            if piece is None:
                print(f"  ERROR: {part}.{pin} sits in a cut hole")
                continue
            pieces.setdefault(piece, set()).add(f"{part}.{pin}")
    found = [p for p in pieces.values() if len(p) > 1]
    ok = True
    for name, pins in WANTED.items():
        if pins not in found:
            ok = False
            for f in found:
                if pins & f and f != pins:
                    extra = f - pins
                    missing = pins - f
                    if extra:
                        print(f"  SHORT: net {name} is joined to {sorted(extra)}")
                    if missing:
                        print(f"  OPEN:  net {name} is missing {sorted(missing)}")
                    break
            else:
                print(f"  OPEN:  net {name} is not connected at all")
    if ok:
        print("  all 5 nets correct, no shorts")


print("layout with no cuts:")
check(set())
print("layout with a cut at row 1, column 5:")
check({(1, 5)})
