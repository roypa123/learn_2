# voltage_walk.py - find a bad connection by measuring the voltage at each point round a loop
from nodal import solve

# Rover's left motor loop: battery + -> fuse -> switch -> connector A -> motor -> connector B -> battery -
parts = ["fuse", "switch", "connector A", "motor", "connector B"]
good = [0.02, 0.01, 0.01, 4.8, 0.01]           # ohms of each part when healthy
bad = [0.02, 0.01, 2.5, 4.8, 0.01]             # connector A is corroded: 2.5 ohm


def walk(resistances):
    # nodes 1..6 along the loop; node 1 is battery +, node 6 is battery - (ground, so we use 0)
    n = len(resistances)
    res = []
    for k, r in enumerate(resistances):
        a = k + 1
        b = k + 2 if k < n - 1 else 0
        res.append((a, b, r))
    v = solve(n, res, [(1, 0, 7.2, 0.15)])
    return v


for label, rs in [("healthy", good), ("connector A corroded", bad)]:
    v = walk(rs)
    i = (v[1] - v[2]) / rs[0]
    print(f"--- {label}: current {i:.3f} A ---")
    pts = [v[k] for k in range(1, len(rs) + 1)] + [0.0]
    for k, name in enumerate(parts):
        drop = pts[k] - pts[k + 1]
        flag = "   <-- too much for a connection!" if name != "motor" and drop > 0.1 else ""
        print(f"  across {name:12s}: {drop:6.3f} V{flag}")
