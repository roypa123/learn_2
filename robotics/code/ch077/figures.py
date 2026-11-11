# Figures for Chapter 77 - Series and parallel circuits.
# Run:  python figures.py      (saves PNG files in ../../images/ch077/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch077")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def battery(ax, x, y, label="12 V"):
    ax.plot([x - 0.4, x + 0.4], [y + 0.15, y + 0.15], color=BLACK, lw=3)
    ax.plot([x - 0.2, x + 0.2], [y - 0.15, y - 0.15], color=BLACK, lw=3)
    ax.text(x - 0.9, y, label, ha="center", va="center", fontsize=11, color=ORANGE)
    ax.text(x + 0.55, y + 0.3, "+", fontsize=12, fontweight="bold")


def resistor(ax, x0, y0, x1, y1, label, color=BLACK):
    # a zigzag between two points
    n = 6
    xs, ys = [x0], [y0]
    dx, dy = (x1 - x0), (y1 - y0)
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; px, py = -uy, ux
    for k in range(1, 2 * n):
        f = k / (2 * n)
        s = 0.18 if k % 2 else -0.18
        xs.append(x0 + dx * f + px * s); ys.append(y0 + dy * f + py * s)
    xs.append(x1); ys.append(y1)
    ax.plot(xs, ys, color=color, lw=2)
    ax.text((x0 + x1) / 2 + px * 0.5, (y0 + y1) / 2 + py * 0.5, label, ha="center", va="center", fontsize=10.5, color=RED)


def arrow(ax, x0, y0, x1, y1, color=GREEN, text="", tx=0, ty=0.25):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", lw=2, color=color))
    if text:
        ax.text((x0 + x1) / 2 + tx, (y0 + y1) / 2 + ty, text, ha="center", fontsize=10, color=color)


# Figure 1: series circuit
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2, 10.5); ax.set_ylim(-1.3, 3.6)
battery(ax, 0, 1.2)
ax.plot([0, 0], [1.35, 3.0], color=BLACK, lw=2); ax.plot([0, 0], [-0.5, 1.05], color=BLACK, lw=2)
ax.plot([0, 1.5], [3.0, 3.0], color=BLACK, lw=2); resistor(ax, 1.5, 3.0, 3.5, 3.0, "R1 = 100")
ax.plot([3.5, 5.0], [3.0, 3.0], color=BLACK, lw=2); resistor(ax, 5.0, 3.0, 7.0, 3.0, "R2 = 200")
ax.plot([7.0, 8.5, 8.5], [3.0, 3.0, 1.5], color=BLACK, lw=2); resistor(ax, 8.5, 1.5, 8.5, -0.5, "R3 = 300")
ax.plot([8.5, 0], [-0.5, -0.5], color=BLACK, lw=2)
arrow(ax, 0.3, 3.3, 1.2, 3.3, text="I = 20 mA", ty=0.2); arrow(ax, 4.0, 3.3, 4.8, 3.3, text="20 mA", ty=0.2)
arrow(ax, 8.8, 0.0, 8.8, -0.4, text="", ); arrow(ax, 5.0, -0.8, 4.0, -0.8, text="20 mA everywhere", ty=-0.45)
ax.text(2.5, 2.3, "2 V", ha="center", color=BLUE, fontsize=11); ax.text(6.0, 2.3, "4 V", ha="center", color=BLUE, fontsize=11)
ax.text(7.6, 0.5, "6 V", ha="center", color=BLUE, fontsize=11)
ax.text(4.2, 1.2, "SERIES: one path, the same current through all;\nthe voltages add up: 2 + 4 + 6 = 12 V;\nR total = 100 + 200 + 300 = 600 ohm", ha="center", fontsize=11)
save(fig, "fig01-series.png")

# Figure 2: parallel circuit
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2, 10.5); ax.set_ylim(-1.3, 3.8)
battery(ax, 0, 1.2)
ax.plot([0, 0], [1.35, 3.0], color=BLACK, lw=2); ax.plot([0, 0], [-0.5, 1.05], color=BLACK, lw=2)
ax.plot([0, 8.5], [3.0, 3.0], color=BLACK, lw=2); ax.plot([0, 8.5], [-0.5, -0.5], color=BLACK, lw=2)
for x, lab, cur in [(3.0, "R1 = 100", "120 mA"), (5.75, "R2 = 200", "60 mA"), (8.5, "R3 = 300", "40 mA")]:
    ax.plot([x, x], [3.0, 2.2], color=BLACK, lw=2); resistor(ax, x, 2.2, x, 0.3, lab); ax.plot([x, x], [0.3, -0.5], color=BLACK, lw=2)
    ax.plot(x, 3.0, "o", color=BLACK, ms=5); ax.plot(x, -0.5, "o", color=BLACK, ms=5)
    arrow(ax, x + 0.3, 2.9, x + 0.3, 2.3, text=cur, tx=0.55, ty=0.0)
arrow(ax, 0.3, 3.3, 1.5, 3.3, text="I = 220 mA", ty=0.2)
ax.text(1.4, 1.2, "PARALLEL: three paths,\nthe same 12 V across each;\nthe currents add up:\n120 + 60 + 40 = 220 mA;\nR total = 12 / 0.22 = 54.5 ohm", ha="center", fontsize=10.5)
save(fig, "fig02-parallel.png")

# Figure 3: reducing a mixed circuit step by step
fig, axes = plt.subplots(1, 3, figsize=(12, 4.4))
for ax in axes:
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2, 7); ax.set_ylim(-1.3, 4.2)
    battery(ax, 0, 1.2)
    ax.plot([0, 0], [1.35, 3.5], color=BLACK, lw=2); ax.plot([0, 0], [-0.5, 1.05], color=BLACK, lw=2)
ax = axes[0]
ax.plot([0, 1.0], [3.5, 3.5], color=BLACK, lw=2); resistor(ax, 1.0, 3.5, 2.8, 3.5, "R1 100")
ax.plot([2.8, 3.5], [3.5, 3.5], color=BLACK, lw=2)
ax.plot([3.5, 3.5], [3.5, 2.8], color=BLACK, lw=2); ax.plot([3.5, 5.5], [2.8, 2.8], color=BLACK, lw=2); ax.plot([3.5, 5.5], [0.5, 0.5], color=BLACK, lw=2)
resistor(ax, 4.0, 2.8, 4.0, 0.5, "R2\n200"); resistor(ax, 5.5, 2.8, 5.5, 0.5, "R3\n300")
ax.plot([3.5, 3.5], [0.5, -0.5], color=BLACK, lw=2); ax.plot([3.5, 1.8], [-0.5, -0.5], color=BLACK, lw=2); resistor(ax, 1.8, -0.5, 0.4, -0.5, "R4 50"); ax.plot([0.4, 0], [-0.5, -0.5], color=BLACK, lw=2)
ax.set_title("1. the circuit", fontsize=11.5)
ax = axes[1]
ax.plot([0, 1.0], [3.5, 3.5], color=BLACK, lw=2); resistor(ax, 1.0, 3.5, 2.8, 3.5, "R1 100")
ax.plot([2.8, 4.5, 4.5], [3.5, 3.5, 2.8], color=BLACK, lw=2); resistor(ax, 4.5, 2.8, 4.5, 0.5, "R23\n120", color=BLUE)
ax.plot([4.5, 4.5, 1.8], [0.5, -0.5, -0.5], color=BLACK, lw=2); resistor(ax, 1.8, -0.5, 0.4, -0.5, "R4 50"); ax.plot([0.4, 0], [-0.5, -0.5], color=BLACK, lw=2)
ax.set_title("2. R2 || R3 = 120 ohm", fontsize=11.5)
ax = axes[2]
ax.plot([0, 2.0, 2.0], [3.5, 3.5, 2.8], color=BLACK, lw=2); resistor(ax, 2.0, 2.8, 2.0, 0.5, "R total\n270", color=BLUE)
ax.plot([2.0, 2.0, 0], [0.5, -0.5, -0.5], color=BLACK, lw=2)
ax.text(4.5, 1.5, "I = 12 / 270\n= 44.4 mA", ha="center", fontsize=11.5, color=GREEN)
ax.set_title("3. all in series: 100 + 120 + 50", fontsize=11.5)
save(fig, "fig03-reduce.png")

# Figure 4: parallel of two resistors - the result is always less than the smaller one
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
n = np.arange(1, 11)
axes[0].plot(n, 1000 / n, "o-", color=BLUE, lw=2, ms=7, mec=BLACK)
for k in [1, 2, 4, 10]:
    axes[0].text(k + 0.15, 1000 / k + 30, f"{1000 / k:.0f}", fontsize=10.5)
axes[0].set_xlabel("number of 1 kohm resistors in parallel"); axes[0].set_ylabel("total resistance (ohm)"); axes[0].grid(alpha=0.3)
axes[0].set_title("n equal resistors in parallel: R / n", fontsize=11.5); axes[0].set_ylim(0, 1100)
r2 = np.linspace(1, 1000, 300)
axes[1].plot(r2, 100 * r2 / (100 + r2), color=BLUE, lw=2.5, label="100 ohm || R2")
axes[1].axhline(100, color=GREY, ls="--", label="never above 100 ohm (the smaller one)")
for r, lab in [(100, "100 || 100 = 50"), (300, "100 || 300 = 75"), (1000, "100 || 1000 = 90.9")]:
    y = 100 * r / (100 + r); axes[1].plot(r, y, "o", color=ORANGE, mec=BLACK, ms=8); axes[1].text(r - 20, y - 14, lab, fontsize=10, ha="right")
axes[1].set_xlabel("R2 (ohm)"); axes[1].set_ylabel("100 ohm in parallel with R2 (ohm)"); axes[1].grid(alpha=0.3); axes[1].legend(fontsize=10, loc="lower right")
axes[1].set_title("a parallel pair is always less than the smaller one", fontsize=11.5); axes[1].set_ylim(0, 115)
save(fig, "fig04-parallel-rules.png")

# Figure 5: battery pack configurations
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
for ax, (s, p, title) in zip(axes, [(4, 1, "4S1P: 14.8 V, 2.5 Ah"), (4, 2, "4S2P: 14.8 V, 5 Ah"), (8, 1, "8S1P: 29.6 V, 2.5 Ah")]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.8, 8 * 1.1 + 0.3); ax.set_ylim(-0.6, 3.2)
    for row in range(p):
        y = 0.3 + row * 1.5
        for k in range(s):
            x = k * 1.1 * (8 / s) if s == 8 else k * 1.1 * 2
            w = 1.1 * (8 / s) - 0.25 if s == 8 else 1.95
            ax.add_patch(plt.Rectangle((x, y), w, 0.9, color=BLUE, ec=BLACK))
            ax.text(x + w / 2, y + 0.45, "3.7 V", ha="center", va="center", fontsize=9, color="white")
            if k < s - 1:
                ax.plot([x + w, x + w + 0.25], [y + 0.45, y + 0.45], color=BLACK, lw=2)
    if p == 2:
        ax.plot([-0.3, -0.3], [0.75, 2.25], color=BLACK, lw=2); ax.plot([-0.3, 0], [0.75, 0.75], color=BLACK, lw=2); ax.plot([-0.3, 0], [2.25, 2.25], color=BLACK, lw=2)
        xe = 8 * 1.1 - 0.05
        ax.plot([xe, xe + 0.3], [0.75, 0.75], color=BLACK, lw=2); ax.plot([xe, xe + 0.3], [2.25, 2.25], color=BLACK, lw=2); ax.plot([xe + 0.3, xe + 0.3], [0.75, 2.25], color=BLACK, lw=2)
    ax.set_title(title, fontsize=11)
fig.suptitle("S = cells in series (voltages add); P = strings in parallel (capacities add); all three use 4 or 8 cells", fontsize=11.5, y=0.02)
save(fig, "fig05-packs.png")

# Figure 6: current split between Rover's two motors with different wire lengths
fig, ax = plt.subplots(figsize=(10, 4.4))
lengths = np.linspace(0.1, 3.0, 50)
r_left = 4.8 + 2 * 0.3 * 0.0336
i_l, i_r = [], []
for L in lengths:
    r_right = 4.8 + 2 * L * 0.0336
    r_pair = 1 / (1 / r_left + 1 / r_right); i_t = 7.2 / (r_pair + 0.15); v = 7.2 - i_t * 0.15
    i_l.append(v / r_left); i_r.append(v / r_right)
ax.plot(lengths, i_l, color=BLUE, lw=2.5, label="left motor (0.3 m wire)")
ax.plot(lengths, i_r, color=ORANGE, lw=2.5, label="right motor (wire length on the axis)")
ax.axvline(0.8, color=GREY, ls="--"); ax.text(0.85, 1.30, "Rover: 0.8 m", fontsize=10.5)
ax.set_xlabel("length of the right motor's wire (m, one way)"); ax.set_ylabel("stall current (A)"); ax.grid(alpha=0.3)
ax.legend(fontsize=10.5); ax.set_ylim(1.25, 1.45)
ax.set_title("two motors in parallel: the one with the longer wire gets a little less current", fontsize=11.5)
save(fig, "fig06-current-split.png")
print("saved 6 figures")
