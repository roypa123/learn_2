# solar_bypass.py - 36 solar cells in series, one of them shaded by a leaf: what do bypass diodes save?
CELLS = 36
CELL_V = 0.5            # each cell's working voltage
SUN_A = 5.0             # current of a cell in full sun
SHADED_A = 1.0          # current the shaded cell can pass
BYPASS_V = 0.4          # a Schottky bypass diode's voltage
GROUP = 12              # one bypass diode across each group of 12 cells

full = CELLS * CELL_V * SUN_A
print(f"full sun: {CELLS * CELL_V:.0f} V x {SUN_A:.0f} A = {full:.0f} W")

no_bypass = CELLS * CELL_V * SHADED_A          # series: every cell carries the shaded cell's current
print(f"one cell shaded, no bypass diodes: {CELLS * CELL_V:.0f} V x {SHADED_A:.0f} A = {no_bypass:.0f} W ({no_bypass / full:.0%})")

# with bypass diodes the controller can choose: run everything at 1 A, or let the shaded group be bypassed at 5 A
option_a = no_bypass
option_b = ((CELLS - GROUP) * CELL_V - BYPASS_V) * SUN_A
best = max(option_a, option_b)
print(f"with bypass diodes: bypass the shaded group -> {(CELLS - GROUP) * CELL_V - BYPASS_V:.1f} V x {SUN_A:.0f} A = {option_b:.0f} W")
print(f"the best of the two choices: {best:.0f} W ({best / full:.0%} of full sun)")
