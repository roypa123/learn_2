# Figures for Chapter 46 - Simultaneous equations.
# Run:  python figures.py      (saves PNG files in ../../images/ch046/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch046")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=3):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=18, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


def axes0(ax):
    ax.axhline(0, color=BLACK, lw=1.2); ax.axvline(0, color=BLACK, lw=1.2); ax.grid(alpha=0.3)


# Figure 1: two lines crossing
x = np.linspace(-1, 11, 10)
fig, ax = plt.subplots(figsize=(8, 6.5))
axes0(ax)
ax.plot(x, 10 - x, color=BLUE, lw=3, label="x + y = 10")
ax.plot(x, x - 2, color=GREEN, lw=3, ls="--", label="x - y = 2")
ax.plot([6], [4], "o", color=RED, ms=12, zorder=5); ax.annotate("(6, 4): on both lines", (6, 4), xytext=(-0.8, 5.0), fontsize=13, color=RED, arrowprops=dict(arrowstyle="-|>", color=RED))
ax.set_xlim(-1, 11); ax.set_ylim(-3, 11); ax.set_aspect("equal"); ax.legend(loc="upper right")
save(fig, "fig01-two-lines.png")

# Figure 2: three cases
fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
x = np.linspace(-1, 5, 10)
axes[0].plot(x, 2 - x, color=BLUE, lw=3); axes[0].plot(x, 0.5 * x, color=GREEN, lw=3, ls="--")
axes[0].plot([4 / 3], [2 / 3], "o", color=RED, ms=10); axes[0].set_title("lines cross: one answer", fontsize=13)
axes[1].plot(x, 2 - x, color=BLUE, lw=3); axes[1].plot(x, 4 - x, color=GREEN, lw=3, ls="--")
axes[1].set_title("parallel: no answer", fontsize=13)
axes[2].plot(x, 2 - x, color=BLUE, lw=6, alpha=0.6); axes[2].plot(x, 2 - x, color=GREEN, lw=2.5, ls="--")
axes[2].set_title("the same line: endless answers", fontsize=13)
for ax in axes:
    axes0(ax); ax.set_xlim(-1, 5); ax.set_ylim(-2, 5)
save(fig, "fig02-three-cases.png")

# Figure 3: wheel speeds for a turn
fig, ax = plt.subplots(figsize=(8, 6))
ax.add_patch(Rectangle((-0.6, -1.0), 1.2, 2.0, fc=ORANGE, ec=BLACK))
ax.add_patch(Rectangle((-0.85, -0.35), 0.25, 0.7, fc=GREY, ec=BLACK)); ax.add_patch(Rectangle((0.6, -0.35), 0.25, 0.7, fc=GREY, ec=BLACK))
arrow(ax, (-0.72, 0.4), (-0.72, 1.6), BLUE); arrow(ax, (0.72, 0.4), (0.72, 2.4), BLUE)
ax.text(-0.95, 1.7, "left\n0.225 m/s", ha="right", fontsize=12.5, color=BLUE); ax.text(0.95, 2.3, "right\n0.375 m/s", fontsize=12.5, color=BLUE)
arrow(ax, (0, 0), (0, 1.6), GREEN, 4); ax.text(0, 1.75, "v = 0.3 m/s", ha="center", fontsize=12.5, color=GREEN, bbox=dict(fc="white", ec="none", pad=1))
th = np.linspace(0.3, 1.5, 50)
ax.plot(-1.5 + 1.0 * np.cos(th + 1.5), 1.6 + 1.0 * np.sin(th + 1.5), color=RED, lw=2.5)
ax.text(-2.9, 2.9, "turn left at 1.0 rad/s", fontsize=12.5, color=RED)
ax.annotate("", xy=(-1.5 + np.cos(3.0), 1.6 + np.sin(3.0)), xytext=(-1.5 + np.cos(2.9), 1.6 + np.sin(2.9)), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
ax.text(0, -1.4, "track width T = 0.15 m", ha="center", fontsize=12)
ax.set_xlim(-3.2, 2.6); ax.set_ylim(-1.7, 3.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-wheel-speeds.png")

# Figure 4: parabola through three sightings
x = np.linspace(-0.5, 7, 300)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, -0.1 * x ** 2 + 0.65 * x + 0.3, color=BLUE, lw=3, label="fitted path: y = -0.1x squared + 0.65x + 0.3")
ax.plot([6, 5, 4], [0.6, 1.05, 1.3], "o", color=BLACK, ms=11, zorder=5, label="three camera sightings")
ax.axvline(0, color=GREY, lw=5); ax.text(-0.1, 1.9, "goal line", fontsize=12, color="#555555")
ax.plot([0], [0.3], "s", color=ORANGE, mec=BLACK, ms=13, zorder=5); ax.text(2.4, 0.12, "crosses at 0.30 m high", fontsize=12.5)
ax.annotate("", xy=(3.2, 1.52), xytext=(4.0, 1.42), arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=2))
ax.set_xlabel("distance from the goal line (m)"); ax.set_ylabel("height (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
ax.set_xlim(7, -0.6); ax.set_ylim(0, 2.2)
save(fig, "fig04-ball-fit.png")

# Figure 5: trilateration
fig, ax = plt.subplots(figsize=(8, 7))
beacons = [(0, 0, 5), (10, 0, 8.0623), (0, 8, 5)]
for (bx, by, r), col in zip(beacons, [BLUE, GREEN, RED]):
    ax.add_patch(Circle((bx, by), r, fill=False, ec=col, lw=2.5, ls="-" if col == BLUE else "--"))
    ax.plot([bx], [by], "^", color=col, ms=13); ax.text(bx + 0.3, by + 0.3, f"beacon ({bx}, {by})", fontsize=12, color=col)
ax.plot([3], [4], "o", color=ORANGE, mec=BLACK, ms=14, zorder=5); ax.text(3.3, 4.3, "robot (3, 4)", fontsize=13)
ax.set_xlim(-6, 12); ax.set_ylim(-6, 14); ax.set_aspect("equal"); ax.grid(alpha=0.3)
save(fig, "fig05-beacons.png")
print("figures saved in", os.path.abspath(OUT))
