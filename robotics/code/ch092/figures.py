# Figures for Chapter 92 - Soldering and building a small circuit.
# Run:  python figures.py      (saves PNG files in ../../images/ch092/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, FancyBboxPatch
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch092")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
COPPER, SOLDER, BOARD = "#C87533", "#B8BCC2", "#E8D9A8"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: the soldering setup
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(FancyBboxPatch((0.3, 0.4), 2.0, 1.2, boxstyle="round,pad=0.05", fc="#DDDDDD", ec=BLACK))
ax.text(1.3, 1.25, "station", ha="center", fontsize=11); ax.text(1.3, 0.75, "350 C", ha="center", fontsize=13, color=RED, family="monospace")
ax.plot([2.3, 3.2], [1.0, 2.6], color=BLACK, lw=2)
ax.add_patch(Polygon([[3.0, 2.4], [3.4, 2.8], [6.2, 3.9], [6.0, 3.5]], closed=True, fc=BLUE, ec=BLACK))
ax.text(4.3, 3.6, "handle", fontsize=10.5, color=BLUE, rotation=22)
ax.add_patch(Polygon([[6.0, 3.5], [6.2, 3.9], [7.4, 4.25], [7.35, 4.05]], closed=True, fc=GREY, ec=BLACK))
ax.add_patch(Polygon([[7.35, 4.05], [7.4, 4.25], [8.0, 4.25], [8.0, 4.2]], closed=True, fc=COPPER, ec=BLACK))
ax.text(7.6, 4.5, "tip (tinned, shiny)", fontsize=10.5, ha="center")
ax.text(6.9, 3.2, "heater inside", fontsize=10, ha="center", color=RED)
ax.add_patch(Rectangle((3.8, 0.4), 1.4, 0.7, fc="#F2D06B", ec=BLACK)); ax.text(4.5, 0.15, "brass wool", ha="center", fontsize=10.5)
ax.plot([6.0, 6.6, 7.2], [0.4, 1.6, 0.4], color=BLACK, lw=2); ax.text(6.6, 0.15, "stand", ha="center", fontsize=10.5)
ax.add_patch(Circle((9.2, 1.2), 0.7, fc=SOLDER, ec=BLACK)); ax.add_patch(Circle((9.2, 1.2), 0.25, fc="white", ec=BLACK))
ax.plot([9.9, 10.6], [1.2, 2.8], color=SOLDER, lw=3); ax.text(9.2, 0.15, "solder wire (flux inside)", ha="center", fontsize=10.5)
ax.text(8.2, 3.0, "fan / fume\nextractor", ha="center", fontsize=10.5, color=GREEN)
ax.annotate("", xy=(8.9, 3.6), xytext=(7.9, 3.6), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
save(fig, "fig01-setup.png")

# Figure 2: the five steps of a through-hole joint
fig, axes = plt.subplots(1, 5, figsize=(13, 3.8))
titles = ["1. touch pad AND lead", "2. feed solder to the joint", "3. take solder away", "4. take iron away", "5. cool, then trim"]
for k, ax in enumerate(axes):
    ax.set_xlim(-2, 2); ax.set_ylim(-1.5, 3); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-2, -0.55), 4, 0.4, fc=BOARD, ec=BLACK))
    ax.add_patch(Rectangle((-0.8, -0.15), 1.6, 0.15, fc=COPPER, ec=BLACK))
    top = 0.9 if k == 4 else 2.6
    ax.add_patch(Rectangle((-0.07, -1.3), 0.14, top + 1.3, fc="#888888", ec=BLACK))
    if k >= 2:
        ax.add_patch(Polygon([[-0.75, 0.0], [-0.07, 0.75], [0.07, 0.75], [0.75, 0.0]], closed=True, fc=SOLDER, ec=BLACK))
    if k == 1:
        ax.add_patch(Polygon([[-0.5, 0.0], [-0.07, 0.45], [0.07, 0.45], [0.5, 0.0]], closed=True, fc=SOLDER, ec=BLACK))
    if k in (0, 1, 2):
        ax.add_patch(Polygon([[-1.9, 1.6], [-1.6, 1.9], [-0.1, 0.35], [-0.35, 0.1]], closed=True, fc=COPPER, ec=BLACK))
    if k == 1:
        ax.plot([1.8, 0.3], [1.8, 0.3], color=SOLDER, lw=4); ax.plot([1.8, 0.3], [1.8, 0.3], color=BLACK, lw=0.5)
    if k == 4:
        ax.plot([0.5, 0.9], [1.6, 2.6], color=GREY, lw=2, ls="--"); ax.text(0.95, 2.3, "cut", fontsize=10)
    ax.set_title(titles[k], fontsize=10.5)
    ax.text(0, -1.45, ["1-2 s", "about 1 s", "", "", "do not move it"][k], ha="center", fontsize=10, color=RED)
save(fig, "fig02-five-steps.png")

# Figure 3: joint temperature against time
T_ROOM, T_SET, T_WET, C_TIP, DT = 25.0, 350.0, 230.0, 2.0, 0.001


def trace(c_j, g_l, g_c, p_max, seconds=6.0):
    t_tip, t_j, out = T_SET, T_ROOM, []
    for _ in range(int(seconds / DT)):
        p = max(0.0, min(p_max, 5.0 * (T_SET - t_tip)))
        flow = g_c * (t_tip - t_j)
        t_tip += (p - flow) / C_TIP * DT
        t_j += (flow - g_l * (t_j - T_ROOM)) / c_j * DT
        out.append(t_j)
    return np.arange(len(out)) * DT, np.array(out)


fig, ax = plt.subplots(figsize=(10, 4.8))
for (c_j, g_l, g_c, p, lab, col, ls) in [(0.05, 0.004, 0.08, 25, "resistor lead, 25 W tinned tip", GREEN, "-"),
                                          (0.4, 0.06, 0.08, 25, "ground-plane pin, 25 W tinned tip", RED, "-"),
                                          (0.4, 0.06, 0.30, 60, "ground-plane pin, 60 W chisel tip", BLUE, "-"),
                                          (0.05, 0.004, 0.02, 25, "resistor lead, dry (untinned) tip", ORANGE, "--")]:
    t, temp = trace(c_j, g_l, g_c, p)
    ax.plot(t, temp, color=col, lw=2.2, ls=ls, label=lab)
ax.axhline(T_WET, color=BLACK, ls=":", lw=1.5); ax.text(4.6, T_WET + 6, "solder wets: 230 C", fontsize=10.5)
ax.axhspan(217, 221, color=GREY, alpha=0.3); ax.text(4.6, 196, "lead-free melts: 217-220 C", fontsize=10.5, color="#555555")
ax.set_xlabel("time after touching the joint (s)"); ax.set_ylabel("joint temperature (C)"); ax.set_ylim(0, 360); ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=10)
save(fig, "fig04-joint-temperature.png")

# Figure 4: good and bad joints in cross-section
fig, axes = plt.subplots(1, 5, figsize=(13, 3.6))
names = ["GOOD: shiny cone,\nconcave sides", "COLD: dull ball,\nnot stuck to pad", "TOO LITTLE:\npad not covered", "TOO MUCH: blob,\nhides the joint", "BRIDGE: joined\nto the next pad"]
for k, ax in enumerate(axes):
    ax.set_xlim(-2, 2); ax.set_ylim(-1.2, 2.4); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-2, -0.55), 4, 0.4, fc=BOARD, ec=BLACK))
    ax.add_patch(Rectangle((-0.8, -0.15), 1.6, 0.15, fc=COPPER, ec=BLACK))
    if k == 4:
        ax.add_patch(Rectangle((1.1, -0.15), 0.9, 0.15, fc=COPPER, ec=BLACK))
    ax.add_patch(Rectangle((-0.07, -1.1), 0.14, 3.1, fc="#888888", ec=BLACK))
    if k == 0:
        xs = np.linspace(-0.75, 0.75, 60); ys = 0.75 * (1 - np.abs(xs) / 0.75) ** 2.2
        ax.fill_between(xs, 0, ys, color=SOLDER, ec=BLACK)
    elif k == 1:
        ax.add_patch(Circle((0, 0.65), 0.55, fc="#9A9A9A", ec=BLACK)); ax.text(0.6, 0.12, "gap", ha="left", fontsize=9, color=RED)
    elif k == 2:
        ax.add_patch(Polygon([[-0.3, 0.0], [-0.07, 0.3], [0.07, 0.3], [0.3, 0.0]], closed=True, fc=SOLDER, ec=BLACK))
    elif k == 3:
        ax.add_patch(Circle((0, 0.85), 0.85, fc=SOLDER, ec=BLACK))
    else:
        xs = np.linspace(-0.75, 1.9, 60); ys = 0.45 + 0.1 * np.sin(xs * 3)
        ax.fill_between(xs, 0, ys, color=SOLDER, ec=BLACK)
    ax.set_title(names[k], fontsize=10.5, color=GREEN if k == 0 else RED)
save(fig, "fig03-good-and-bad.png")

# Figure 5: wire gauge
RHO = 1.68e-8
awgs = [30, 26, 24, 22, 20, 18, 16]
ohm = [RHO / (math.pi * (0.127 * 92 ** ((36 - a) / 39) / 1000) ** 2 / 4) for a in awgs]
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
axes[0].bar([str(a) for a in awgs], [o * 1000 for o in ohm], color=BLUE)
axes[0].set_xlabel("AWG (bigger number = thinner wire)"); axes[0].set_ylabel("milliohms per metre"); axes[0].grid(axis="y", alpha=0.3)
axes[0].set_title("resistance of copper wire", fontsize=11.5)
heat = [3.1 ** 2 * o for o in ohm]
cols = [RED if h > 0.5 else GREEN for h in heat]
axes[1].bar([str(a) for a in awgs], heat, color=cols); axes[1].axhline(0.5, color=BLACK, ls=":")
axes[1].text(6.4, 0.6, "0.5 W per metre", ha="right", fontsize=10)
axes[1].set_xlabel("AWG"); axes[1].set_ylabel("watts of heat per metre"); axes[1].grid(axis="y", alpha=0.3)
axes[1].set_title("heat in the wire at Rover's 3.1 A start current", fontsize=11.5)
for i, h in enumerate(heat):
    axes[1].text(i, h + 0.05, f"{h:.2f}", ha="center", fontsize=9)
save(fig, "fig05-wire-gauge.png")

# Figure 6: the stripboard layout
fig, ax = plt.subplots(figsize=(11, 5))
ROWS, COLS = 4, 10
ax.set_xlim(-1.2, COLS + 0.5); ax.set_ylim(-1.0, ROWS + 1.4); ax.invert_yaxis(); ax.set_aspect("equal"); ax.axis("off")
for r in range(ROWS):
    ax.add_patch(Rectangle((-0.45, r - 0.3), COLS - 0.1, 0.6, fc=COPPER, ec="none", alpha=0.45))
    for c in range(COLS):
        ax.add_patch(Circle((c, r), 0.09, fc="white", ec=BLACK, lw=0.6))
    ax.text(-0.75, r, f"row {r}", ha="right", va="center", fontsize=10)
for c in range(COLS):
    ax.text(c, -0.6, str(c), ha="center", fontsize=9, color="#555555")
ax.add_patch(Rectangle((4.75, 0.68), 0.5, 0.64, fc="white", ec=RED, lw=2)); ax.plot([4.8, 5.2], [0.75, 1.25], color=RED, lw=2); ax.plot([4.8, 5.2], [1.25, 0.75], color=RED, lw=2)
ax.text(5.0, 5.0, "cut at row 1, col 5", color=RED, ha="center", fontsize=10.5)
ax.annotate("", xy=(5.0, 1.35), xytext=(5.0, 4.7), arrowprops=dict(arrowstyle="->", color=RED))
for (r1, c1, r2, c2, lab, col) in [(1, 2, 3, 2, "R1 1k", BLUE), (3, 4, 2, 4, "R2 2k", BLUE), (0, 7, 1, 7, "R3 330", BLUE), (1, 8, 2, 8, "LED1", RED)]:
    ax.plot([c1, c2], [r1, r2], color=col, lw=5, solid_capstyle="round", alpha=0.85)
    ax.text(c1 + 0.2, (r1 + r2) / 2, lab, fontsize=10, color=col, va="center")
for (r, c) in [(0, 0), (1, 0), (2, 0)]:
    ax.add_patch(Rectangle((c - 0.2, r - 0.2), 0.4, 0.4, fc=BLACK))
for (r, c) in [(2, 9), (3, 9)]:
    ax.add_patch(Rectangle((c - 0.2, r - 0.2), 0.4, 0.4, fc=BLACK))
ax.text(0, 4.1, "J1 to Uno:\n5V, TX, GND", ha="center", fontsize=10)
ax.text(9.0, 4.1, "J2 to Pi:\nGND, RX", ha="center", fontsize=10)
save(fig, "fig06-stripboard.png")
print("saved 6 figures")
