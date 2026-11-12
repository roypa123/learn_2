# bridge.py - a Wheatstone bridge turns a tiny change in a strain gauge into a voltage we can amplify
from nodal import solve

EXCITE_V = 5.0
R = 350.0                  # each arm of the bridge, and the gauge when unstrained
GAUGE_FACTOR = 2.0         # the gauge's resistance changes by 2 x the strain


def bridge_output(strain):
    gauge = R * (1 + GAUGE_FACTOR * strain)
    # nodes: 1 = top (+5 V), 2 = left middle, 3 = right middle
    v = solve(3, [(1, 2, R), (2, 0, gauge), (1, 3, R), (3, 0, R)], [(1, 0, EXCITE_V, 1e-9)])
    return v[2] - v[3]


print(f"{'strain':>10s} {'gauge ohms':>11s} {'output':>10s} {'simple formula':>15s}")
for micro in [0, 100, 250, 500, 1000, 2000]:
    strain = micro * 1e-6
    out = bridge_output(strain)
    simple = EXCITE_V * GAUGE_FACTOR * strain / 4         # good for small strains
    print(f"{micro:7d} ue {R * (1 + GAUGE_FACTOR * strain):11.3f} {out * 1000:7.3f} mV {simple * 1000:12.3f} mV")

print()
print("one ADC step on a 5 V Arduino is 4.88 mV: even 2,000 microstrain gives under 5 mV,")
print("so the bridge output is amplified about 128 times first (Chapter 128)")
