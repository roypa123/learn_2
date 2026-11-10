# Figures for Chapter 41 - Algebra part 2.
# Run:  python figures.py      (saves PNG files in ../../images/ch041/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch041")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=3))


def box(ax, x, y, w, h, text, face, size=15):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


# Figure 1: doing and undoing
fig, ax = plt.subplots(figsize=(12, 4.6))
vals = ["x = 4", "12", "14"]
for i, v in enumerate(vals):
    box(ax, i * 4.2, 2.0, 2.4, 1.2, v, L_ORANGE if i == 0 else L_BLUE, 17)
for i, t in enumerate(["x 3", "+ 2"]):
    arrow(ax, (i * 4.2 + 2.5, 3.0), (i * 4.2 + 4.1, 3.0), BLUE)
    ax.text(i * 4.2 + 3.3, 3.2, t, ha="center", fontsize=15, color=BLUE)
for i, t in enumerate(["/ 3", "- 2"]):
    arrow(ax, (i * 4.2 + 4.1, 2.2), (i * 4.2 + 2.5, 2.2), RED)
    ax.text(i * 4.2 + 3.3, 1.65, t, ha="center", fontsize=15, color=RED)
ax.text(5.3, 4.0, "Building the left side: do these, from left to right", ha="center", fontsize=13.5, color=BLUE)
ax.text(5.3, 0.95, "Solving for x: undo them, from right to left", ha="center", fontsize=13.5, color=RED)
ax.set_xlim(-0.2, 11); ax.set_ylim(0.7, 4.5); ax.axis("off")
save(fig, "fig01-do-and-undo.png")

# Figure 2: inequality number line
fig, ax = plt.subplots(figsize=(11, 3))
ax.add_patch(FancyArrowPatch((-0.4, 0), (10.4, 0), arrowstyle="<|-|>", mutation_scale=16, color=BLACK, lw=1.5))
for n in range(0, 11):
    ax.plot([n, n], [-0.12, 0.12], color=BLACK, lw=1.5)
    ax.text(n, -0.45, str(n), ha="center", fontsize=12)
ax.plot([0, 6], [0.5, 0.5], color=GREEN, lw=6, solid_capstyle="butt")
ax.plot([6], [0.5], "o", ms=14, color=GREEN, mec=BLACK)
ax.text(3, 0.75, "safe: t <= 6 seconds", ha="center", fontsize=13, color=GREEN)
ax.text(8.2, 0.75, "not safe", ha="center", fontsize=13, color=RED)
ax.plot([6.3, 10.2], [0.5, 0.5], color=RED, lw=3, ls=":")
ax.set_xlim(-0.6, 10.7); ax.set_ylim(-0.75, 1.1); ax.axis("off")
save(fig, "fig02-inequality.png")

# Figure 3: arm and part
t = np.linspace(0, 5, 100)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(t, 0.5 * t, color=ORANGE, lw=3, label="arm: x = 0.5 t")
ax.plot(t, 0.6 + 0.2 * t, color=BLUE, lw=3, ls="--", label="part on the belt: x = 0.6 + 0.2 t")
ax.plot([2], [1.0], "o", color=BLACK, ms=11, zorder=5)
ax.annotate("they meet: t = 2 s, x = 1.0 m", (2, 1.0), xytext=(2.5, 0.45), fontsize=12.5, arrowprops=dict(arrowstyle="-|>", color=BLACK))
ax.axhline(1.5, color=GREY, lw=2.5); ax.text(0.1, 1.55, "end of the belt, 1.5 m", fontsize=12)
ax.set_xlabel("time (s)"); ax.set_ylabel("position along the belt (m)"); ax.grid(alpha=0.3); ax.legend(loc="lower right")
ax.set_xlim(0, 5); ax.set_ylim(0, 2.0)
save(fig, "fig03-intercept.png")

# Figure 4: range against hover
E = 74 * 0.8 * 3600
h = np.linspace(0, 1100, 100)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(h, (E - 200 * h) * 12 / 360 / 1000, color=BLUE, lw=3)
ax.plot([60], [(E - 200 * 60) * 12 / 360 / 1000], "o", color=ORANGE, mec=BLACK, ms=12)
ax.annotate("60 s hover: 6.70 km", (60, 6.70), xytext=(170, 7.2), fontsize=12.5, arrowprops=dict(arrowstyle="-|>", color=BLACK))
ax.set_xlabel("hover time at the delivery (s)"); ax.set_ylabel("furthest delivery (km)"); ax.grid(alpha=0.3)
ax.set_xlim(0, 1100); ax.set_ylim(0, 8)
save(fig, "fig04-drone-range.png")
print("figures saved in", os.path.abspath(OUT))
