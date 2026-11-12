# pack_builder.py - building a battery pack from cells: S in series, P in parallel
CELL_V = 3.7              # nominal
CELL_AH = 2.5
CELL_OHM = 0.020          # internal resistance of one cell
POWER_W = 600.0           # the drone's motors at full throttle

print(f"one cell: {CELL_V} V, {CELL_AH} Ah, {CELL_OHM} ohm inside")
print(f"{'pack':6s} {'volts':>6s} {'Ah':>5s} {'Wh':>6s} {'ohm':>7s} {'amps':>6s} {'sag':>7s} {'heat':>7s}")
for s, p in [(4, 1), (4, 2), (8, 1), (2, 4), (6, 2)]:
    volts = s * CELL_V                       # series: voltages add
    ah = p * CELL_AH                         # parallel: capacities add
    wh = volts * ah
    ohm = s * CELL_OHM / p                   # series adds, parallel divides
    amps = POWER_W / volts                   # the current needed for 600 W
    sag = amps * ohm                         # V = I x R inside the pack
    heat = amps ** 2 * ohm                   # I^2 R inside the pack
    print(f"{s}S{p}P   {volts:6.1f} {ah:5.1f} {wh:6.0f} {ohm:7.3f} {amps:6.1f} {sag:6.2f} V {heat:5.0f} W")

print()
print("4S2P, 8S1P and 2S4P all store 74 Wh and all make 66 W of heat inside at 600 W.")
print("The 8S pack needs half the current of 4S2P, so its wires can be much thinner (Chapter 75).")
