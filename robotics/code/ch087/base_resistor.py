# base_resistor.py - choose the base resistor so the transistor is fully on, with a safe pin current
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
V_PIN = 4.7                # an Arduino pin's high voltage under a few mA of load (Chapter 82)
V_BE = 0.7                 # base-emitter voltage of a silicon transistor (a diode, Chapter 86)
FORCED_BETA = 20           # we give 5x more base current than beta_min=100 would need: certain saturation


def next_lower_e12(r):
    """The largest E12 value not above r (a smaller resistor gives MORE base current: the safe direction)."""
    best = None
    scale = 1.0
    while scale <= r * 10:
        for v in E12:
            if v * scale <= r + 1e-9:
                best = v * scale
        scale *= 10
    return best


loads = [("5 V relay coil", 0.071), ("small DC fan", 0.150), ("12 V lamp", 0.300), ("LED strip", 0.500)]
print(f"{'load':16s} {'Ic':>7s} {'Ib needed':>10s} {'exact Rb':>9s} {'use':>7s} {'pin current':>12s} {'verdict':>22s}")
for name, ic in loads:
    ib = ic / FORCED_BETA
    rb = (V_PIN - V_BE) / ib
    use = next_lower_e12(rb)
    pin = (V_PIN - V_BE) / use
    part = "2N2222 / BC337 is fine" if pin <= 0.020 else "TOO MUCH for a pin: MOSFET (Ch 88)"
    print(f"{name:16s} {ic * 1000:5.0f} mA {ib * 1000:7.2f} mA {rb:8.0f} {use:6.0f} {pin * 1000:9.2f} mA  {part}")
print()
print("the pin may give at most 20 mA: a plain transistor can switch up to about 0.3 A from an Arduino pin")
print("add 10 kohm from base to ground so the transistor stays OFF while the pin floats during start-up (Chapter 83)")
