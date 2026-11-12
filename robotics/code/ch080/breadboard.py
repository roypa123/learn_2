# breadboard.py - which holes of a breadboard are joined? Find the nets, catch mistakes, then solve the circuit
from nodal import solve


def strip_of(hole):
    """The metal strip a hole belongs to. 'c12' -> 'L12' (a-e of row 12), 'h12' -> 'R12', 'T+5' -> 'T+'."""
    if hole[0] in "TB":                       # power rails along the Top and Bottom edges
        return hole[:2]
    column, row = hole[0], hole[1:]
    return ("L" if column in "abcde" else "R") + row


def find_nets(parts, wires):
    """Group strips that are joined by jumper wires. Returns a dict: strip -> net number."""
    strips = set()
    for _, _, pins in parts:
        strips.update(strip_of(h) for h in pins)
    for a, b in wires:
        strips.update([strip_of(a), strip_of(b)])
    net = {s: k for k, s in enumerate(sorted(strips))}
    changed = True
    while changed:                            # keep merging until nothing changes
        changed = False
        for a, b in wires:
            na, nb = net[strip_of(a)], net[strip_of(b)]
            if na != nb:
                low, high = min(na, nb), max(na, nb)
                for s in net:
                    if net[s] == high:
                        net[s] = low
                changed = True
    return net


def check(parts, wires, supply_plus, supply_minus):
    net = find_nets(parts, wires)
    problems = []
    if net[strip_of(supply_plus)] == net[strip_of(supply_minus)]:
        problems.append("SHORT CIRCUIT: the supply's + and - are on the same net")
    for name, _, pins in parts:
        if len({net[strip_of(h)] for h in pins}) == 1:
            problems.append(f"{name}: all its legs are on one net, so it does nothing (it is shorted out)")
    used = {}
    for name, _, pins in parts:
        for h in pins:
            used.setdefault(net[strip_of(h)], []).append(name)
    for n, names in used.items():
        if len(names) == 1 and n not in (net[strip_of(supply_plus)], net[strip_of(supply_minus)]):
            problems.append(f"{names[0]}: one leg is on a net that goes nowhere (an open circuit)")
    return net, problems


def show(title, parts, wires):
    print(f"--- {title} ---")
    net, problems = check(parts, wires, "T+1", "T-1")
    for p in problems:
        print("  PROBLEM:", p)
    if problems:
        return
    # number the nets for the solver: ground's net becomes node 0
    gnd = net[strip_of("T-1")]
    ids = {gnd: 0}
    for n in sorted(set(net.values())):
        if n not in ids:
            ids[n] = len(ids)
    resistors = [(ids[net[strip_of(p[0])]], ids[net[strip_of(p[1])]], ohms) for _, ohms, p in parts]
    plus = ids[net[strip_of("T+1")]]
    v = solve(len(ids) - 1, resistors, [(plus, 0, 5.0, 1e-9)])
    print("  no problems found")
    for name, ohms, pins in parts:
        a, b = ids[net[strip_of(pins[0])]], ids[net[strip_of(pins[1])]]
        print(f"  {name:4s} {ohms:6.0f} ohm: {v[a]:5.3f} V -> {v[b]:5.3f} V, current {(v[a] - v[b]) / ohms * 1000:6.3f} mA")


# a 10 k over 10 k divider in row 10, and a 1 k resistor as the 'load' from the tap to ground
good_parts = [("R1", 10000, ["a5", "a10"]), ("R2", 10000, ["b10", "b15"]), ("R3", 1000, ["c10", "c20"])]
good_wires = [("T+1", "e5"), ("e15", "T-3"), ("e20", "T-5")]
show("correct layout", good_parts, good_wires)

# mistake 1: R2 put in with both legs in row 10
show("R2 in one row", [("R1", 10000, ["a5", "a10"]), ("R2", 10000, ["b10", "d10"]), ("R3", 1000, ["c10", "c20"])], good_wires)

# mistake 2: a wire to the bottom of R2 forgotten
show("missing wire", good_parts, [("T+1", "e5"), ("e20", "T-5")])

# mistake 3: a jumper meant for the tap lands on the - rail and the + rail joined to it by accident
show("rails joined", good_parts, good_wires + [("T+7", "T-7")])
