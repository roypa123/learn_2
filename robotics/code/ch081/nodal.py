# nodal.py - solve any circuit of resistors and batteries with Kirchhoff's current law and NumPy
import numpy as np


def solve(n_nodes, resistors, sources):
    """
    Nodes are numbered 1 .. n_nodes; node 0 is ground (0 V).
    resistors: list of (a, b, ohms) joining node a and node b.
    sources:   list of (a, b, volts, ohms): a battery whose + is at node a and - at node b,
               with its internal resistance in series.
    Returns the list of node voltages, with ground first.
    """
    g = np.zeros((n_nodes + 1, n_nodes + 1))       # the conductance matrix
    i = np.zeros(n_nodes + 1)                      # the currents pushed into each node
    for a, b, r in resistors:
        g[a, a] += 1 / r; g[b, b] += 1 / r
        g[a, b] -= 1 / r; g[b, a] -= 1 / r
    for a, b, e, r in sources:                     # a battery with resistance = a current e/r in parallel with r
        g[a, a] += 1 / r; g[b, b] += 1 / r
        g[a, b] -= 1 / r; g[b, a] -= 1 / r
        i[a] += e / r; i[b] -= e / r
    v = np.linalg.solve(g[1:, 1:], i[1:])          # drop the ground row and column, then solve
    return [0.0] + list(v)


if __name__ == "__main__":
    # test 1: the Chapter 77 circuit. Nodes: 1 = battery +, 2 = node A, 3 = node B
    v = solve(3, [(1, 2, 100), (2, 3, 200), (2, 3, 300), (3, 0, 50)], [(1, 0, 12.0, 1e-9)])
    print("Chapter 77 circuit:", ", ".join(f"V{k} = {x:.3f} V" for k, x in enumerate(v)))
    print(f"  battery current = {(v[1] - v[2]) / 100 * 1000:.1f} mA (Chapter 77 found 44.4 mA)")

    # test 2: a bridge that cannot be shrunk with series and parallel rules
    # nodes: 1 = top, 2 = left middle, 3 = right middle; a 5 ohm resistor joins the two middles
    v = solve(3, [(1, 2, 10), (1, 3, 20), (2, 0, 30), (3, 0, 40), (2, 3, 5)], [(1, 0, 10.0, 1e-9)])
    print("bridge:", ", ".join(f"V{k} = {x:.3f} V" for k, x in enumerate(v)))
    print(f"  current through the middle 5 ohm resistor: {(v[2] - v[3]) / 5 * 1000:+.1f} mA")
