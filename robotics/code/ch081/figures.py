# Figures for Chapter 81 - The multimeter: measuring safely.
# Run:  python figures.py      (saves PNG files in ../../images/ch081/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from nodal import solve

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch081")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: the meter - display, dial, sockets
fig, ax = plt.subplots(figsize=(10, 7))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-6, 9); ax.set_ylim(-6.3, 6.3)
ax.add_patch(plt.Rectangle((-3, -6), 6, 12, color=ORANGE, ec=BLACK, lw=2, alpha=0.8))
ax.add_patch(plt.Rectangle((-2.4, 3.2), 4.8, 2.2, color="#C8D8C0", ec=BLACK))
ax.text(0, 4.3, "7.38", ha="center", va="center", fontsize=34, family="monospace")
ax.text(1.9, 3.5, "V", fontsize=12)
ax.add_patch(plt.Circle((0, 0), 2.2, color=L_GREY, ec=BLACK, lw=2))
ax.add_patch(plt.Circle((0, 0), 0.6, color=GREY, ec=BLACK))
ang = math.radians(115); ax.plot([0, 1.9 * math.cos(ang)], [0, 1.9 * math.sin(ang)], color=BLACK, lw=4)
for a, lab in [(150, "OFF"), (115, "V="), (80, "V~"), (45, "ohm"), (10, "beep"), (-30, "diode"), (-70, "mA"), (-110, "10A"), (-150, "A~")]:
    r = math.radians(a)
    ax.text(2.75 * math.cos(r), 2.75 * math.sin(r), lab, ha="center", va="center", fontsize=9.5)
for x, lab, col in [(-2.0, "10A", RED), (-0.7, "mA", RED), (0.7, "COM", BLACK), (2.0, "V ohm", RED)]:
    ax.add_patch(plt.Circle((x, -4.6), 0.35, color=col, ec=BLACK))
    ax.text(x, -5.3, lab, ha="center", fontsize=9.5)
ax.text(4.2, 4.3, "display: 2000 counts\n(up to 1999)", fontsize=10.5, va="center")
ax.text(4.2, 0.6, "dial: choose WHAT to\nmeasure and the RANGE", fontsize=10.5, va="center")
ax.text(4.2, -3.2, "COM: the black lead,\nalways\n\nV ohm: the red lead for\nvolts, ohms, beep, diode\n\nmA and 10A: the red lead\nONLY for current,\neach with its own fuse", fontsize=10, va="center")
ax.annotate("", xy=(2.5, -4.6), xytext=(4.1, -3.6), arrowprops=dict(arrowstyle="->", color=BLACK))
save(fig, "fig01-meter.png")

# Figure 2: how to connect for V, I and R
fig, axes = plt.subplots(1, 3, figsize=(13, 4.6))
for ax, title in zip(axes, ["VOLTAGE: across the part,\ncircuit ON", "CURRENT: break the loop,\nmeter IN it, circuit ON",
                            "RESISTANCE: part ALONE,\npower OFF"]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 7); ax.set_ylim(-1.5, 5.5); ax.set_title(title, fontsize=11)
# common loop drawing helper
def loop(ax, gap=False, power=True):
    if power:
        ax.plot([0, 0], [0, 1.6], color=BLACK, lw=2); ax.plot([-0.35, 0.35], [1.75, 1.75], color=BLACK, lw=3); ax.plot([-0.18, 0.18], [1.55, 1.55], color=BLACK, lw=3)
        ax.plot([0, 0], [1.75, 4], color=BLACK, lw=2)
    ax.plot([0, 2.0], [4, 4], color=BLACK, lw=2)
    if gap:
        ax.plot([3.6, 5], [4, 4], color=BLACK, lw=2)
    else:
        ax.plot([2.0, 5], [4, 4], color=BLACK, lw=2)
    ax.plot([5, 5], [4, 2.8], color=BLACK, lw=2); ax.add_patch(plt.Rectangle((4.6, 1.2), 0.8, 1.6, color=L_ORANGE, ec=BLACK))
    ax.text(5, 2.0, "R", ha="center", va="center"); ax.plot([5, 5], [1.2, 0], color=BLACK, lw=2); ax.plot([5, 0], [0, 0], color=BLACK, lw=2)


def meter(ax, x, y, text):
    ax.add_patch(plt.Rectangle((x - 0.7, y - 0.45), 1.4, 0.9, color=ORANGE, ec=BLACK))
    ax.text(x, y, text, ha="center", va="center", fontsize=10)


loop(axes[0]); meter(axes[0], 3.0, 2.0, "V"); axes[0].plot([3.7, 5], [2.3, 2.6], color=RED, lw=2); axes[0].plot([3.7, 5], [1.7, 1.2], color=BLACK, lw=2)
axes[0].text(3.0, -0.8, "meter in PARALLEL", ha="center", color=BLUE)
loop(axes[1], gap=True); meter(axes[1], 2.8, 4.0, "A"); axes[1].text(2.8, 4.75, "red lead in mA or 10A", ha="center", fontsize=9, color=RED)
axes[1].text(3.0, -0.8, "meter in SERIES", ha="center", color=BLUE)
axes[2].add_patch(plt.Rectangle((1.4, 2.0), 1.6, 0.8, color=L_ORANGE, ec=BLACK)); axes[2].text(2.2, 2.4, "R", ha="center", va="center")
meter(axes[2], 2.2, 0.4, "ohm"); axes[2].plot([1.4, 1.0, 1.0, 1.5], [2.4, 2.4, 0.4, 0.4], color=RED, lw=2); axes[2].plot([3.0, 3.4, 3.4, 2.9], [2.4, 2.4, 0.4, 0.4], color=BLACK, lw=2)
axes[2].text(3.0, -0.8, "the meter makes its own tiny current", ha="center", color=BLUE, fontsize=10)
save(fig, "fig02-how-to-connect.png")

# Figure 3: meter loading
fig, ax = plt.subplots(figsize=(10, 4.8))
R = np.logspace(2, 7, 200)
for rm, col, lab in [(10e6, BLUE, "10 Mohm digital meter"), (1e6, ORANGE, "1 Mohm meter"), (200e3, RED, "old analog meter on its 10 V range (200 kohm)")]:
    rout = R / 2
    err = -rout / (rout + rm) * 100
    ax.semilogx(R, err, color=col, lw=2.5, label=lab)
ax.axhline(-1, color=GREY, ls="--"); ax.text(150, -3.5, "1% error", fontsize=10)
ax.set_xticks([100, 1e3, 1e4, 1e5, 1e6, 1e7]); ax.set_xticklabels(["100", "1 k", "10 k", "100 k", "1 M", "10 M"])
ax.set_xlabel("R1 = R2 of the divider being measured (ohm)"); ax.set_ylabel("error of the reading (%)"); ax.grid(alpha=0.3, which="both")
ax.legend(loc="lower left", fontsize=10.5); ax.set_ylim(-80, 3)
ax.set_title("the meter loads the circuit: fine for small resistances, wrong for big ones", fontsize=11.5)
save(fig, "fig03-meter-loading.png")

# Figure 4: accuracy on two ranges
fig, ax = plt.subplots(figsize=(10, 4.8))
v = np.linspace(0.05, 20, 400)
for fs, col in [(2.0, GREEN), (20.0, BLUE), (200.0, RED)]:
    vv = v[v < fs]
    err = (0.005 * vv + 2 * fs / 2000) / vv * 100
    ax.loglog(vv, err, color=col, lw=2.5, label=f"{fs:g} V range")
ax.set_xlabel("true voltage (V)"); ax.set_ylabel("possible error (% of the reading)"); ax.grid(alpha=0.3, which="both")
ax.set_xticks([0.1, 1, 10]); ax.set_xticklabels(["0.1", "1", "10"]); ax.set_yticks([0.5, 1, 10, 100]); ax.set_yticklabels(["0.5", "1", "10", "100"])
ax.legend(fontsize=10.5); ax.set_title("each range is most accurate near its top: use the smallest range that does not overflow", fontsize=11)
save(fig, "fig04-accuracy.png")

# Figure 5: the voltage walk
fig, ax = plt.subplots(figsize=(10, 4.8))
names = ["battery +", "after fuse", "after switch", "after conn. A", "after motor", "after conn. B"]
for rs, col, lab, mk in [([0.02, 0.01, 0.01, 4.8, 0.01], GREEN, "healthy", "o"), ([0.02, 0.01, 2.5, 4.8, 0.01], RED, "connector A corroded", "s")]:
    n = len(rs); res = [(k + 1, k + 2 if k < n - 1 else 0, r) for k, r in enumerate(rs)]
    vv = solve(n, res, [(1, 0, 7.2, 0.15)])
    pts = [vv[k] for k in range(1, n + 1)] + [0.0]
    ax.plot(range(6), pts, mk + "-", color=col, lw=2.5, ms=8, label=lab)
ax.annotate("2.4 V lost in one connector", xy=(2.5, 5.5), xytext=(0.3, 3.0), arrowprops=dict(arrowstyle="->"), fontsize=10.5, color=RED)
ax.set_xticks(range(6)); ax.set_xticklabels(names, fontsize=10); ax.set_ylabel("volts above battery -"); ax.grid(alpha=0.3); ax.legend(fontsize=10.5)
ax.set_title("walk the black lead on battery -, the red lead along the loop: the big step is the fault", fontsize=11)
save(fig, "fig05-voltage-walk.png")

# Figure 6: internal resistance from the readings
fig, ax = plt.subplots(figsize=(10, 4.6))
I = [0, 7.57 / 22, 7.51 / 10, 7.39 / 4.7]; V = [7.62, 7.57, 7.51, 7.39]
ax.plot(I, V, "o", color=ORANGE, mec=BLACK, ms=10, label="meter readings")
ii = np.linspace(0, 3.2, 50)
ax.plot(ii, 7.62 - 0.146 * ii, color=BLUE, lw=2.5, label="V = 7.62 - 0.146 x I")
ax.plot(3.1, 7.62 - 0.146 * 3.1, "s", color=RED, ms=9); ax.text(3.0, 7.28, "motor start\n3.1 A: 7.17 V", ha="right", fontsize=10.5)
ax.set_xlabel("current drawn (A)"); ax.set_ylabel("battery terminal voltage (V)"); ax.grid(alpha=0.3); ax.legend(fontsize=10.5)
ax.set_title("the slope of the line is the battery's internal resistance: 0.146 ohm", fontsize=11.5)
save(fig, "fig06-internal-resistance.png")
print("saved 6 figures")
