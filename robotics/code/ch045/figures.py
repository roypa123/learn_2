# Figures for Chapter 45 - Quadratic equations and parabolas.
# Run:  python figures.py      (saves PNG files in ../../images/ch045/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch045")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def axes0(ax):
    ax.axhline(0, color=BLACK, lw=1.2); ax.axvline(0, color=BLACK, lw=1.2); ax.grid(alpha=0.3)


# Figure 1: parts of a parabola
x = np.linspace(-2.5, 4.5, 300)
fig, ax = plt.subplots(figsize=(9, 6.5))
axes0(ax)
ax.plot(x, x ** 2 - 2 * x - 3, color=BLUE, lw=3, label="y = x squared - 2x - 3")
ax.axvline(1, color=GREY, ls="--", lw=2); ax.text(1.1, 6.3, "line of symmetry: x = 1", fontsize=12, color="#555555")
ax.plot([1], [-4], "o", color=RED, ms=11, zorder=5); ax.text(1.2, -4.6, "vertex (1, -4)", fontsize=12.5, color=RED)
ax.plot([-1, 3], [0, 0], "o", color=GREEN, ms=11, zorder=5)
ax.text(-2.4, 0.4, "root x = -1", fontsize=12.5, color=GREEN); ax.text(3.25, -0.8, "root x = 3", fontsize=12.5, color=GREEN)
ax.plot([0], [-3], "s", color=BLACK, ms=9, zorder=5); ax.text(-1.9, -3.1, "y-intercept (0, -3)", fontsize=12)
ax.set_xlim(-2.5, 4.5); ax.set_ylim(-5.5, 8); ax.legend(loc="upper left")
save(fig, "fig01-parts.png")

# Figure 2: effect of a, and of shifting
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
x = np.linspace(-3, 3, 300)
for a, col, st in [(2, RED, ":"), (1, BLUE, "-"), (0.5, GREEN, "--"), (-1, ORANGE, "-.")]:
    axes[0].plot(x, a * x ** 2, color=col, ls=st, lw=2.8, label=f"y = {a} x squared")
axes[0].set_title("a sets the width, and up or down", fontsize=13)
for (h, k), col, st in [((0, 0), BLUE, "-"), ((2, 0), GREEN, "--"), ((0, -3), RED, ":"), ((-1, 2), ORANGE, "-.")]:
    axes[1].plot(x, (x - h) ** 2 + k, color=col, ls=st, lw=2.8, label=f"vertex at ({h}, {k})")
axes[1].set_title("y = (x - h) squared + k moves the vertex", fontsize=13)
for ax in axes:
    axes0(ax); ax.set_xlim(-3, 3); ax.set_ylim(-5, 8); ax.legend(loc="lower right", fontsize=11)
save(fig, "fig02-a-and-shift.png")

# Figure 3: discriminant cases
fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
x = np.linspace(-1, 5, 300)
cases = [(1, -5, 6, "disc = 1 > 0: two roots"), (1, -4, 4, "disc = 0: one root"), (1, -4, 6, "disc = -8 < 0: no root")]
for ax, (a, b, c, t) in zip(axes, cases):
    axes0(ax); ax.plot(x, a * x ** 2 + b * x + c, color=BLUE, lw=3); ax.set_title(t, fontsize=13)
    ax.set_xlim(-1, 5); ax.set_ylim(-1.5, 5)
axes[0].plot([2, 3], [0, 0], "o", color=GREEN, ms=10); axes[1].plot([2], [0], "o", color=GREEN, ms=10)
save(fig, "fig03-discriminant.png")

# Figure 4: completing the square, x^2 + 6x
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
ax = axes[0]
ax.add_patch(Rectangle((0, 0), 4, 4, fc=L_BLUE, ec=BLACK)); ax.text(2, 2, "x squared", ha="center", va="center", fontsize=14)
ax.add_patch(Rectangle((4, 0), 2.4, 4, fc=L_GREEN, ec=BLACK)); ax.text(5.2, 2, "6x", ha="center", va="center", fontsize=14)
ax.text(2, 4.25, "x", ha="center", fontsize=13); ax.text(5.2, 4.25, "6", ha="center", fontsize=13)
ax.set_title("x squared + 6x", fontsize=13); ax.set_xlim(-0.5, 7.5); ax.set_ylim(-3, 5); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
ax.add_patch(Rectangle((0, 1.2), 4, 4, fc=L_BLUE, ec=BLACK)); ax.text(2, 3.2, "x squared", ha="center", va="center", fontsize=14)
ax.add_patch(Rectangle((4, 1.2), 1.2, 4, fc=L_GREEN, ec=BLACK)); ax.text(4.6, 3.2, "3x", ha="center", va="center", fontsize=13)
ax.add_patch(Rectangle((0, 0), 4, 1.2, fc=L_GREEN, ec=BLACK)); ax.text(2, 0.6, "3x", ha="center", va="center", fontsize=13)
ax.add_patch(Rectangle((4, 0), 1.2, 1.2, fc=L_ORANGE, ec=BLACK, ls="--")); ax.text(4.6, 0.6, "9", ha="center", va="center", fontsize=13)
ax.text(2, 5.45, "x", ha="center", fontsize=13); ax.text(4.6, 5.45, "3", ha="center", fontsize=13)
ax.text(2.6, -1.2, "add the missing 9: a full square (x + 3) squared", ha="center", fontsize=12.5)
ax.set_title("split 6x into two halves", fontsize=13); ax.set_xlim(-0.5, 7.5); ax.set_ylim(-2, 6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-complete-square.png")

# Figure 5: stopping distance
v = np.linspace(0, 4, 300)
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(v, 0.3 * v, color=GREEN, ls="--", lw=2.2, label="reaction part: 0.3 v (a straight line)")
ax.plot(v, v ** 2 / 3, color=ORANGE, ls=":", lw=2.6, label="braking part: v squared / 3 (a parabola)")
ax.plot(v, 0.3 * v + v ** 2 / 3, color=BLUE, lw=3, label="total stopping distance")
ax.axhline(2, color=BLACK, ls="--", lw=1.8)
ax.plot([2.0405], [2], "o", color=RED, ms=11, zorder=5)
ax.annotate("2.0405 m/s", (2.0405, 2), xytext=(2.4, 1.0), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("speed v (m/s)"); ax.set_ylabel("distance (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
ax.set_xlim(0, 4); ax.set_ylim(0, 6.5)
save(fig, "fig05-stopping.png")

# Figure 6: the throw
t = np.linspace(0, 0.8628, 300)
xs = 2.4 * t; ys = 0.5 + 4 * t - 0.5 * 9.81 * t ** 2
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(xs, ys, color=BLUE, lw=3, label="path of the parcel")
ax.add_patch(Rectangle((-0.25, 0), 0.3, 0.5, fc=ORANGE, ec=BLACK)); ax.text(-0.1, 0.62, "robot", ha="center", fontsize=11.5)
ax.add_patch(Rectangle((1.85, 0), 0.3, 0.3, fc=L_GREY, ec=BLACK)); ax.text(2.0, 0.12, "bin", ha="center", fontsize=11.5)
ax.plot([0.979], [1.315], "o", color=RED, ms=10); ax.text(1.05, 1.36, "highest: 1.315 m", fontsize=12, color=RED)
ax.plot([2.071], [0.3], "o", color=GREEN, ms=10); ax.text(2.2, 0.42, "x = 2.071 m", fontsize=12, color=GREEN)
ax.axhline(0, color=BLACK, lw=1.5)
ax.set_xlabel("across (m)"); ax.set_ylabel("height (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper right")
ax.set_xlim(-0.4, 2.8); ax.set_ylim(0, 1.6); ax.set_aspect("equal")
save(fig, "fig06-throw.png")
print("figures saved in", os.path.abspath(OUT))
