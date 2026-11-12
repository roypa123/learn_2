# lipo_model.py - a simple model of one lithium cell: its resting voltage at each state of charge, and its sag
import numpy as np

# measured-style table: state of charge (0 = empty, 1 = full) -> resting ('open-circuit') voltage of one cell
SOC_POINTS = [0.00, 0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
OCV_POINTS = [3.00, 3.45, 3.62, 3.70, 3.75, 3.79, 3.83, 3.87, 3.93, 4.00, 4.08, 4.20]


def ocv(soc):
    """Resting voltage of one cell at a state of charge, by straight lines between the table's points (Chapter 43)."""
    return float(np.interp(soc, SOC_POINTS, OCV_POINTS))


def soc_from_ocv(v):
    """The reverse: state of charge from a resting voltage."""
    return float(np.interp(v, OCV_POINTS, SOC_POINTS))


if __name__ == "__main__":
    print(f"{'charge left':>12s} {'resting voltage':>16s}")
    for s in [1.0, 0.9, 0.8, 0.5, 0.2, 0.1, 0.05, 0.0]:
        print(f"{s:11.0%} {ocv(s):13.2f} V")
    print()
    r_cell = 0.005                 # a good 5,000 mAh drone cell: about 5 milliohms inside
    print("a cell at 50% charge, under different currents (sag = I x R):")
    for amps in [0, 5, 25, 60, 125]:
        v = ocv(0.5) - amps * r_cell
        print(f"  {amps:4d} A: {v:.3f} V -> a voltage-only estimate would say {soc_from_ocv(v):.0%} charge left")
