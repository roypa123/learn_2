# Figures for Chapter 34 — NumPy part 1: arrays.
# Run:  python figures.py      (saves PNG files in ../../images/ch034/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch034")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


def cells(ax, x0, y, items, face=L_BLUE, w=1.0, h=0.8, size=13):
    for i, v in enumerate(items):
        c = face[i] if isinstance(face, list) else face
        ax.add_patch(Rectangle((x0 + i * w, y), w, h, fc=c, ec=BLACK, lw=1.3))
        ax.text(x0 + i * w + w / 2, y + h / 2, str(v), ha="center", va="center", fontsize=size, family=MONO, weight="bold")


# ---------- Figure 1: list against array ----------
fig, ax = plt.subplots(figsize=(13.5, 4.8))
ax.text(0.1, 4.45, "list * 2", fontsize=15, family=MONO, weight="bold", color=RED)
cells(ax, 0.1, 3.4, [1, 2, 3])
arrow(ax, (3.3, 3.8), (4.3, 3.8), RED)
cells(ax, 4.4, 3.4, [1, 2, 3, 1, 2, 3], face=L_RED)
ax.text(10.8, 3.8, "the list is REPEATED", fontsize=13, color=RED, weight="bold", va="center")
ax.text(0.1, 2.1, "array * 2", fontsize=15, family=MONO, weight="bold", color=GREEN)
cells(ax, 0.1, 1.05, [1, 2, 3])
arrow(ax, (3.3, 1.45), (4.3, 1.45), GREEN)
cells(ax, 4.4, 1.05, [2, 4, 6], face=L_GREEN)
ax.text(7.7, 1.45, "every item is multiplied", fontsize=13, color=GREEN, weight="bold", va="center")
ax.set_xlim(0, 14.6); ax.set_ylim(0.8, 4.8); ax.axis("off")
save(fig, "fig01-list-and-array.png")

# ---------- Figure 2: rows and columns ----------
fig, ax = plt.subplots(figsize=(12.5, 5.0))
M = [[1, 2, 3], [4, 5, 6]]
for r in range(2):
    for c in range(3):
        col = L_GREEN if c == 1 else (L_ORANGE if r == 1 else L_BLUE)
        ax.add_patch(Rectangle((3 + c * 1.5, 2.6 - r * 1.2), 1.5, 1.2, fc=col, ec=BLACK, lw=1.5))
        ax.text(3.75 + c * 1.5, 3.2 - r * 1.2, str(M[r][c]), ha="center", va="center", fontsize=18, family=MONO, weight="bold")
for r in range(2):
    ax.text(2.7, 3.2 - r * 1.2, f"row {r}", ha="right", va="center", fontsize=13, weight="bold")
for c in range(3):
    ax.text(3.75 + c * 1.5, 4.05, f"col {c}", ha="center", fontsize=13, weight="bold")
ax.text(8.1, 3.2, "m[1]  or  m[1, :]\nthe whole of row 1 (orange)", fontsize=13, va="center", family=MONO)
ax.text(8.1, 1.7, "m[:, 1]\nthe whole of column 1 (green)", fontsize=13, va="center", family=MONO)
ax.text(5.25, 0.85, "m[1, 2] is 6      m.shape is (2, 3): 2 rows, 3 columns", ha="center", fontsize=13.5, family=MONO, weight="bold")
ax.set_xlim(0.6, 13); ax.set_ylim(0.6, 4.4); ax.axis("off")
save(fig, "fig02-rows-and-columns.png")

# ---------- Figure 3: a mask ----------
fig, ax = plt.subplots(figsize=(13.5, 4.8))
s = [0.52, 0.51, 0.0, 0.53, 3.91, 0.5, 0.52]
ax.text(0.1, 4.0, "samples", fontsize=13, family=MONO, weight="bold", va="center")
cells(ax, 2.8, 3.6, s, w=1.35)
ax.text(0.1, 2.5, "valid", fontsize=13, family=MONO, weight="bold", va="center")
m = [0.02 <= v <= 4.0 for v in s]
cells(ax, 2.8, 2.1, ["True" if b else "False" for b in m], face=[L_GREEN if b else L_RED for b in m], w=1.35, size=12)
ax.text(0.1, 1.0, "samples[valid]", fontsize=13, family=MONO, weight="bold", va="center")
cells(ax, 2.8, 0.6, [v for v, b in zip(s, m) if b], face=L_GREEN, w=1.35)
ax.text(2.8, 4.75, "a comparison gives one True or False per item; indexing with it keeps the True ones", fontsize=13)
ax.set_xlim(0, 12.5); ax.set_ylim(0.4, 5.1); ax.axis("off")
save(fig, "fig03-a-mask.png")

# ---------- Figure 4: a lidar scan ----------
a = np.radians(np.arange(0, 360, 45))
r = np.array([2.0, 1.5, 1.0, 0.8, 1.0, np.inf, 3.0, 2.5])
fig, ax = plt.subplots(figsize=(8.5, 7.5))
for ang, rr in zip(a, r):
    rr2 = 3.4 if np.isinf(rr) else rr
    ax.plot([0, rr2 * np.cos(ang)], [0, rr2 * np.sin(ang)], color=GREY if np.isinf(rr) else RED, lw=1.5, ls=":" if np.isinf(rr) else "-")
hit = np.isfinite(r)
ax.plot(r[hit] * np.cos(a[hit]), r[hit] * np.sin(a[hit]), "o", color=BLUE, ms=11, label="the points we calculate")
ax.plot(0, 0, "s", color=ORANGE, ms=18, mec=BLACK, label="the robot")
ax.text(-1.3, -2.45, "no return (inf)", fontsize=12, color=GREY, ha="center")
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.legend(loc="upper left", framealpha=1)
save(fig, "fig04-lidar-scan.png")

# ---------- Figure 5: axis ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 4.6))
for ax, title, a0 in [(axes[0], "m.sum(axis=0): down each column", True), (axes[1], "m.sum(axis=1): across each row", False)]:
    for r in range(2):
        for c in range(3):
            ax.add_patch(Rectangle((c, 1 - r), 1, 1, fc=L_BLUE, ec=BLACK, lw=1.3))
            ax.text(c + 0.5, 1.5 - r, str(M[r][c]), ha="center", va="center", fontsize=16, family=MONO, weight="bold")
    if a0:
        for c in range(3):
            arrow(ax, (c + 0.82, 1.82), (c + 0.82, 0.1), ORANGE, 2.2)
            ax.text(c + 0.5, -0.4, str(M[0][c] + M[1][c]), ha="center", va="center", fontsize=17, family=MONO, weight="bold", color=GREEN)
    else:
        for r in range(2):
            arrow(ax, (0.12, 1.2 - r), (2.9, 1.2 - r), ORANGE, 2.2)
            ax.text(3.45, 1.5 - r, str(sum(M[r])), ha="center", va="center", fontsize=17, family=MONO, weight="bold", color=GREEN)
    ax.set_title(title, fontsize=14, weight="bold", family=MONO)
    ax.set_xlim(-0.3, 4.0); ax.set_ylim(-0.8, 2.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-axis.png")
print("figures saved in", os.path.abspath(OUT))
