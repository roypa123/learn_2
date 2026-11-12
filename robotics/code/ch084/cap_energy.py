# cap_energy.py - charge and energy stored in some capacitors: Q = C x V, E = 1/2 x C x V^2
caps = [
    # name, farads, volts
    ("decoupling capacitor next to a chip", 100e-9, 5.0),
    ("bulk capacitor on Rover's motor driver", 470e-6, 7.2),
    ("big bulk capacitor on a drone ESC", 1000e-6, 25.2),
    ("supercapacitor (small backup cell)", 10.0, 2.7),
    ("camera flash capacitor", 120e-6, 330.0),
]
print(f"{'capacitor':40s} {'C':>10s} {'V':>7s} {'charge':>10s} {'energy':>10s}")
for name, c, v in caps:
    q = c * v
    e = 0.5 * c * v * v
    c_txt = f"{c * 1e9:.0f} nF" if c < 1e-6 else (f"{c * 1e6:.0f} uF" if c < 1 else f"{c:.0f} F")
    print(f"{name:40s} {c_txt:>10s} {v:5.1f} V {q:8.4g} C {e:8.4g} J")

print()
print("for comparison: one AA cell stores about 10,000 J; Chapter 73's static spark was 0.011 J")
