# diode_iv.py - how much current flows through three kinds of diode at each voltage?
import math

N_VT = 0.050                       # the steepness (about 0.026 V x 2 for a real diode at room temperature)


def silicon(v):
    """A silicon rectifier diode: 1 A at 0.85 V forward; blocks backwards (a tiny leak) until about -1000 V."""
    return 1.0 * math.exp((v - 0.85) / N_VT) if v > 0 else -1e-6


def schottky(v):
    """A Schottky diode: 1 A at 0.45 V forward, but it leaks more backwards."""
    return 1.0 * math.exp((v - 0.45) / N_VT) if v > 0 else -1e-4


def zener(v, vz=5.1):
    """A 5.1 V Zener: like silicon forwards, and it conducts backwards once the reverse voltage reaches vz."""
    if v >= 0:
        return silicon(v)
    return -0.010 * math.exp((-v - vz) / 0.05) if -v > vz - 0.4 else -1e-6


print(f"{'voltage':>8s} {'silicon':>12s} {'Schottky':>12s} {'5.1 V Zener':>12s}")
for v in [-6.0, -5.1, -5.0, -1.0, 0.0, 0.3, 0.45, 0.6, 0.7, 0.85]:
    row = [silicon(v), schottky(v), zener(v)]
    print(f"{v:6.2f} V " + " ".join(f"{i * 1000:10.3f} mA" if abs(i) <= 1.0 else f"{'over 1 A':>13s}" for i in row))
print()
print("forward: almost nothing until about 0.5 V (silicon) or 0.2 V (Schottky), then a steep rise")
print("reverse: only a tiny leak, except the Zener, which holds the voltage at about 5.1 V")
