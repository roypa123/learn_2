# led_model.py - an LED's current rises steeply with voltage; a resistor makes the current steady
import math

N_VT = 0.052                 # the steepness: the current is multiplied by e (2.72) for every 0.052 V more


def led_current(v, vf_at_20ma):
    """A simple exponential LED model: 20 mA at its rated forward voltage."""
    return 0.020 * math.exp((v - vf_at_20ma) / N_VT)


def solve_with_resistor(supply, r, vf_at_20ma):
    """Find the LED voltage where the resistor's current equals the LED's current (bisection, Chapter 44)."""
    lo, hi = 0.0, supply
    for _ in range(60):
        mid = (lo + hi) / 2
        if led_current(mid, vf_at_20ma) > (supply - mid) / r:   # LED wants more than the resistor allows
            hi = mid
        else:
            lo = mid
    return (supply - lo) / r, lo


print("1) an LED connected straight to a supply (no resistor): the current explodes")
for v in [1.8, 1.9, 2.0, 2.1, 2.2, 2.3]:
    print(f"   {v:.1f} V -> {led_current(v, 2.0) * 1000:9.1f} mA")

print()
print("2) three red LEDs from the same bag (Vf at 20 mA = 1.9, 2.0, 2.1 V)")
print(f"   {'':14s} {'Vf 1.9 V':>10s} {'Vf 2.0 V':>10s} {'Vf 2.1 V':>10s}")
for supply, r in [(2.1, 0.5), (5.0, 150.0), (12.0, 500.0)]:
    row = []
    for vf in [1.9, 2.0, 2.1]:
        i, _ = solve_with_resistor(supply, r, vf)
        row.append(f"{i * 1000:7.1f} mA")
    print(f"   {supply:4.1f} V, {r:5.1f} ohm  " + "  ".join(row))
print()
print("the more of the supply the resistor takes, the less the LED's own variation matters")
