# short_circuit.py - what happens to the current as the resistance gets smaller and smaller
V = 7.2
FUSE_A = 4.0                     # Rover's fuse (Chapter 7)
BATTERY_INSIDE = 0.15            # the battery's own resistance in ohms (Chapter 89 explains it)

print(f"{'resistance':>12s} {'current':>10s} {'fuse?':>8s}")
for r in [100, 10, 3, 1, 0.3, 0.1, 0.03, 0.01, 0.0]:
    i = V / (r + BATTERY_INSIDE)         # the battery's own resistance is always in the loop
    blows = "BLOWS" if i > FUSE_A else "ok"
    print(f"{r:10.2f} ohms {i:8.2f} A {blows:>8s}")

print()
print(f"with a perfect battery (no resistance inside), a 0.01 ohm short would draw {V / 0.01:.0f} A")
print(f"the real battery's {BATTERY_INSIDE} ohms limits any short to about {V / BATTERY_INSIDE:.0f} A: still 12 times the fuse")
