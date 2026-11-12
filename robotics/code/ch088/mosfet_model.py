# mosfet_model.py - how much does a MOSFET resist, for each gate voltage? Logic-level vs standard parts
def r_on(v_gs, v_th, r_min, v_full):
    """A simple model: off below the threshold, then the resistance falls until the gate reaches v_full."""
    if v_gs <= v_th:
        return float("inf")
    if v_gs >= v_full:
        return r_min
    return r_min * (v_full - v_th) / (v_gs - v_th)        # falls as the gate rises above the threshold


PARTS = {
    "logic-level (IRLZ44N-like)": dict(v_th=1.5, r_min=0.025, v_full=4.0),
    "standard (IRF540-like)": dict(v_th=3.0, r_min=0.044, v_full=10.0),
}
LOAD_A = 5.0
print(f"switching {LOAD_A:.0f} A: resistance and heat for each gate voltage")
print(f"{'gate':>6s}" + "".join(f"{name:>32s}" for name in PARTS))
for vg in [2.0, 3.3, 4.5, 5.0, 10.0]:
    cells = []
    for p in PARTS.values():
        r = r_on(vg, **p)
        cells.append("OFF" if r == float("inf") else f"{r * 1000:6.0f} mohm, {LOAD_A ** 2 * r:5.2f} W")
    print(f"{vg:5.1f} V" + "".join(f"{c:>32s}" for c in cells))
print()
print("from a 5 V Arduino pin only the logic-level part is fully on; the standard part needs about 10 V on its gate")
