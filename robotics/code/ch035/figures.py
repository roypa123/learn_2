# Figures for Chapter 35 — NumPy part 2: array maths and speed.
# Run:  python figures.py      (saves PNG files in ../../images/ch035/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch035")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw, zorder=3))


def grid(ax, x0, y0, M, face=L_BLUE, w=0.9, h=0.8, ghost=False):
    for r, row in enumerate(M):
        for c, v in enumerate(row):
            ax.add_patch(Rectangle((x0 + c * w, y0 - r * h), w, h, fc=face, ec=GREY if ghost else BLACK, lw=1.2, ls="--" if ghost else "-"))
            ax.text(x0 + c * w + w / 2, y0 - r * h + h / 2, str(v), ha="center", va="center", fontsize=13, family=MONO,
                    weight="bold", color=GREY if ghost else BLACK)


# ---------- Figure 1: speed ----------
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.barh(["NumPy", "Python loop"], [8.3, 314.4], color=[GREEN, RED], ec=BLACK)
ax.text(314.4 + 3, 1, "314 ms", va="center", fontsize=13, weight="bold")
ax.text(8.3 + 3, 0, "8.3 ms", va="center", fontsize=13, weight="bold")
ax.set_xlabel("time to work out one million values (ms): one real run")
ax.set_xlim(0, 360); ax.grid(axis="x", alpha=0.3)
save(fig, "fig01-speed.png")

# ---------- Figure 2: broadcasting ----------
fig, ax = plt.subplots(figsize=(13.5, 6.0))
M = [[1, 2, 3], [4, 5, 6]]
ax.text(0.1, 6.0, "m + 10", fontsize=14, family=MONO, weight="bold", color=BLUE)
grid(ax, 0.1, 4.8, M)
ax.text(3.15, 4.5, "+", fontsize=20, weight="bold", ha="center", va="center")
grid(ax, 3.6, 4.8, [[10, "", ""], ["", "", ""]], face=L_ORANGE)
grid(ax, 3.6, 4.8, [["", 10, 10], [10, 10, 10]], face=L_ORANGE, ghost=True)
ax.text(6.65, 4.5, "=", fontsize=20, weight="bold", ha="center", va="center")
grid(ax, 7.1, 4.8, [[11, 12, 13], [14, 15, 16]], face=L_GREEN)
ax.text(10.1, 4.6, "one number is\nstretched to fit", fontsize=12.5, va="center", color=ORANGE, weight="bold")
ax.text(0.1, 2.75, "m + [10, 20, 30]", fontsize=14, family=MONO, weight="bold", color=BLUE)
grid(ax, 0.1, 1.55, M)
ax.text(3.15, 1.25, "+", fontsize=20, weight="bold", ha="center", va="center")
grid(ax, 3.6, 1.55, [[10, 20, 30], ["", "", ""]], face=L_ORANGE)
grid(ax, 3.6, 1.55, [["", "", ""], [10, 20, 30]], face=L_ORANGE, ghost=True)
ax.text(6.65, 1.25, "=", fontsize=20, weight="bold", ha="center", va="center")
grid(ax, 7.1, 1.55, [[11, 22, 33], [14, 25, 36]], face=L_GREEN)
ax.text(10.1, 1.35, "one row is\nrepeated to fit", fontsize=12.5, va="center", color=ORANGE, weight="bold")
ax.set_xlim(0, 13); ax.set_ylim(0.5, 6.4); ax.axis("off")
save(fig, "fig02-broadcasting.png")

# ---------- Figure 3: matrix times vector ----------
fig, ax = plt.subplots(figsize=(13, 4.4))
grid(ax, 0.5, 2.3, [[1, 2], [3, 4]], face=L_BLUE, w=1, h=1)
ax.text(3.0, 2.3, "@", fontsize=22, weight="bold", ha="center", va="center", family=MONO)
grid(ax, 3.6, 2.3, [[1], [2]], face=L_ORANGE, w=1, h=1)
ax.text(5.15, 2.3, "=", fontsize=22, weight="bold", ha="center", va="center")
grid(ax, 5.6, 2.3, [[5], [11]], face=L_GREEN, w=1, h=1)
ax.text(7.3, 2.85, "first row:   1 x 1 + 2 x 2 = 5", fontsize=14, family=MONO, va="center")
ax.text(7.3, 1.85, "second row:  3 x 1 + 4 x 2 = 11", fontsize=14, family=MONO, va="center")
ax.text(6.4, 0.7, "Each row of the matrix is multiplied with the vector, and the products are added.", ha="center", fontsize=13, style="italic")
ax.set_xlim(0.2, 13.4); ax.set_ylim(0.4, 3.6); ax.axis("off")
save(fig, "fig03-matrix-times-vector.png")

# ---------- Figure 4: the robot frame and the map frame ----------
rx, ry, deg = 2.0, 1.0, 30.0
th = np.radians(deg)
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
pr = np.array([[1.0, 0.0], [1.0, 1.0], [0.0, 2.0]])
pw = (R @ pr.T).T + [rx, ry]
fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.0))
ax = axes[0]
arrow(ax, (0, 0), (1.5, 0), RED, 3); arrow(ax, (0, 0), (0, 1.5), GREEN, 3)
ax.text(1.55, -0.13, "forward", color=RED, fontsize=12, weight="bold"); ax.text(0.05, 1.53, "left", color=GREEN, fontsize=12, weight="bold")
ax.plot(pr[:, 0], pr[:, 1], "o", color=BLUE, ms=12)
for p in pr:
    ax.text(p[0] + 0.07, p[1] + 0.08, f"({p[0]:.0f}, {p[1]:.0f})", fontsize=12)
ax.add_patch(Polygon([(0.3, 0), (-0.2, 0.2), (-0.2, -0.2)], closed=True, fc=ORANGE, ec=BLACK, zorder=4))
ax.set_title("What the robot sees (robot frame)", fontsize=14, weight="bold"); ax.set_xlim(-0.8, 2.4); ax.set_ylim(-0.8, 2.6); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax = axes[1]
ax.plot(pw[:, 0], pw[:, 1], "o", color=BLUE, ms=12)
for p in pw:
    ax.text(p[0] + 0.07, p[1] + 0.08, f"({p[0]:.2f}, {p[1]:.2f})", fontsize=11.5)
fx, fy = R @ [1.0, 0.0]; lx, ly = R @ [0.0, 1.0]
arrow(ax, (rx, ry), (rx + 1.0 * fx, ry + 1.0 * fy), RED, 3); arrow(ax, (rx, ry), (rx + 1.0 * lx, ry + 1.0 * ly), GREEN, 3)
tri = (R @ np.array([[0.3, 0], [-0.2, 0.2], [-0.2, -0.2]]).T).T + [rx, ry]
ax.add_patch(Polygon(tri, closed=True, fc=ORANGE, ec=BLACK, zorder=4))
ax.set_title("The same points on the map (world frame)", fontsize=14, weight="bold"); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
ax.set_xlim(0, 4); ax.set_ylim(0, 3.6); ax.set_aspect("equal"); ax.grid(alpha=0.3)
save(fig, "fig04-robot-and-world-frames.png")

# ---------- Figure 5: Monte Carlo with many runs ----------
gains = ["1.0", "2.0", "3.0"]
m500 = [6 / 5, 231 / 5, 442 / 5]
m100k = [1.849, 49.306, 88.922]
x = np.arange(3)
fig, ax = plt.subplots(figsize=(9.5, 4.8))
ax.bar(x - 0.2, m500, 0.4, color=GREY, ec=BLACK, label="500 runs (Chapter 31)")
ax.bar(x + 0.2, m100k, 0.4, color=BLUE, ec=BLACK, label="100,000 runs (NumPy)")
for i in range(3):
    ax.text(x[i] - 0.2, m500[i] + 1.5, f"{m500[i]:.1f}%", ha="center", fontsize=11.5)
    ax.text(x[i] + 0.2, m100k[i] + 1.5, f"{m100k[i]:.1f}%", ha="center", fontsize=11.5)
ax.set_xticks(x); ax.set_xticklabels(gains); ax.set_xlabel("gain"); ax.set_ylabel("runs with a near miss (%)"); ax.set_ylim(0, 105); ax.grid(axis="y", alpha=0.3); ax.legend(loc="upper left", framealpha=1)
save(fig, "fig05-monte-carlo-bars.png")
print("figures saved in", os.path.abspath(OUT))
