# Figures for Chapter 42 - Coordinates and the number plane.
# Run:  python figures.py      (saves PNG files in ../../images/ch042/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch042")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=3))


def axes_plane(ax, lim=6):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_aspect("equal")
    ax.set_xticks(range(-lim + 1, lim)); ax.set_yticks(range(-lim + 1, lim)); ax.grid(alpha=0.35)
    ax.axhline(0, color=BLACK, lw=1.5); ax.axvline(0, color=BLACK, lw=1.5)
    ax.text(lim - 0.3, 0.3, "x", fontsize=14, weight="bold"); ax.text(0.3, lim - 0.6, "y", fontsize=14, weight="bold")


# Figure 1: the plane with points and quadrants
fig, ax = plt.subplots(figsize=(7.5, 7.5))
axes_plane(ax)
for (x, y), q in zip([(3, 2), (-4, 1), (-2, -3), (5, -1)], ["I", "II", "III", "IV"]):
    ax.plot([x], [y], "o", color=BLUE, ms=10, zorder=4)
    ax.text(x + 0.25, y + 0.25, f"({x}, {y})", fontsize=12.5, color=BLUE)
for (x, y), q in zip([(3.5, 4.5), (-3.5, 4.5), (-3.5, -4.5), (3.5, -4.5)], ["I", "II", "III", "IV"]):
    ax.text(x, y, q, fontsize=20, color=GREY, ha="center", va="center", weight="bold")
ax.plot([0], [0], "s", color=BLACK, ms=8); ax.text(-1.6, -0.6, "origin (0, 0)", fontsize=12)
ax.plot([3, 3], [0, 2], color=BLUE, ls=":", lw=1.5); ax.plot([0, 3], [2, 2], color=BLUE, ls=":", lw=1.5)
save(fig, "fig01-plane.png")

# Figure 2: grid distance against straight line
fig, ax = plt.subplots(figsize=(7.5, 6.2))
ax.set_xlim(0, 6); ax.set_ylim(0, 5); ax.set_aspect("equal"); ax.grid(alpha=0.35)
ax.plot([1, 5, 5], [1, 1, 4], color=GREEN, lw=3.5, label="grid route: 4 + 3 = 7")
ax.plot([1, 5], [1, 4], color=BLUE, lw=2.5, ls="--", label="straight line: 5 (Chapter 48)")
ax.plot([1], [1], "o", color=ORANGE, mec=BLACK, ms=13, zorder=5); ax.text(0.55, 1.25, "a (1, 1)", fontsize=12.5)
ax.plot([5], [4], "o", color=ORANGE, mec=BLACK, ms=13, zorder=5); ax.text(4.3, 4.35, "b (5, 4)", fontsize=12.5)
ax.plot([3], [2.5], "x", color=BLACK, ms=12, mew=3); ax.text(2.1, 2.75, "midpoint (3, 2.5)", fontsize=12)
ax.text(3, 0.55, "dx = 5 - 1 = 4", ha="center", fontsize=12.5, color=GREEN)
ax.text(5.15, 2.5, "dy = 4 - 1 = 3", rotation=90, va="center", fontsize=12.5, color=GREEN)
ax.legend(loc="upper left", fontsize=11.5)
save(fig, "fig02-distance.png")

# Figure 3: rows and columns against x and y
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
ax = axes[0]
for r in range(4):
    for c in range(5):
        ax.add_patch(Rectangle((c, 3 - r), 1, 1, fc="white", ec=BLACK))
        ax.text(c + 0.5, 3 - r + 0.5, f"{r},{c}", ha="center", va="center", fontsize=11)
ax.add_patch(Rectangle((3, 2), 1, 1, fc=L_ORANGE, ec=BLACK)); ax.text(3.5, 2.5, "1,3", ha="center", va="center", fontsize=11)
ax.set_title("a list of rows: row first, row 0 at the TOP", fontsize=12.5)
ax.set_xlim(-0.2, 5.2); ax.set_ylim(-0.2, 4.2); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
for x in range(5):
    for y in range(4):
        ax.add_patch(Rectangle((x, y), 1, 1, fc="white", ec=BLACK))
ax.add_patch(Rectangle((3, 1), 1, 1, fc=L_ORANGE, ec=BLACK)); ax.text(3.5, 1.5, "x=3\ny=1", ha="center", va="center", fontsize=11)
arrow(ax, (0, 0), (5.4, 0), BLUE); arrow(ax, (0, 0), (0, 4.4), BLUE)
ax.text(5.5, -0.1, "x", fontsize=13, color=BLUE); ax.text(-0.1, 4.5, "y", fontsize=13, color=BLUE)
ax.set_title("maths and maps: x first, y = 0 at the BOTTOM", fontsize=12.5)
ax.set_xlim(-0.4, 5.9); ax.set_ylim(-0.4, 4.8); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-rows-and-xy.png")

# Figure 4: translate, flip, scale
shape = [(0, 0), (2, 0), (2, 1), (0, 1)]
fig, ax = plt.subplots(figsize=(8, 7))
axes_plane(ax)
ax.add_patch(Polygon(shape, closed=True, fc=ORANGE, ec=BLACK, alpha=0.85, label="start"))
ax.add_patch(Polygon([(x + 3, y + 2) for x, y in shape], closed=True, fc=L_BLUE, ec=BLUE, lw=2, label="translated by (3, 2)"))
ax.add_patch(Polygon([(x, -y) for x, y in shape], closed=True, fc=L_GREEN, ec=GREEN, lw=2, hatch="//", label="flipped over the x axis"))
ax.add_patch(Polygon([(-x * 2, y * 2) for x, y in shape], closed=True, fc="none", ec=RED, lw=2.5, ls="--", label="scaled by 2 (drawn on the left)"))
arrow(ax, (1, 0.5), (4, 2.5), BLUE, 1.8)
ax.legend(loc="lower left", fontsize=11)
save(fig, "fig04-move-shape.png")

# Figure 5: robot axes, 3D and from above
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
ax = axes[0]
ax.add_patch(Rectangle((-0.6, -0.45), 1.2, 0.9, fc=ORANGE, ec=BLACK))
arrow(ax, (0, 0), (1.8, 0), RED, 3); arrow(ax, (0, 0), (0, 1.5), GREEN, 3)
ax.text(1.85, -0.1, "x: forward", fontsize=13, color=RED); ax.text(0.1, 1.55, "y: to the left", fontsize=13, color=GREEN)
ax.text(-0.25, -0.75, "z: up, out of the page", fontsize=12.5, color=BLUE)
ax.plot([0], [0], "o", color=BLUE, ms=9, zorder=5)
ax.set_title("a robot seen from above", fontsize=13)
ax.set_xlim(-1.2, 3.6); ax.set_ylim(-1.1, 2.0); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
o = (0, 0)
arrow(ax, o, (2.0, 0), RED, 3); arrow(ax, o, (-1.1, -1.0), GREEN, 3); arrow(ax, o, (0, 2.0), BLUE, 3)
ax.text(2.05, -0.1, "x", fontsize=14, color=RED); ax.text(-1.35, -1.2, "y", fontsize=14, color=GREEN); ax.text(-0.05, 2.1, "z", fontsize=14, color=BLUE)
px, py, pz = 1.5, 0.6, 1.2
P = (px - 0.55 * py, -0.5 * py + pz)
ax.plot([0, px, px - 0.55 * py, P[0]], [0, 0, -0.5 * py, P[1]], color=GREY, ls=":", lw=2)
ax.plot([P[0]], [P[1]], "o", color=BLACK, ms=9); ax.text(P[0] + 0.1, P[1] + 0.1, "(1.5, 0.6, 1.2)", fontsize=12.5)
ax.set_title("three numbers for a point in space", fontsize=13)
ax.set_xlim(-1.6, 3.0); ax.set_ylim(-1.4, 2.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-robot-axes.png")

# Figure 6: warehouse routes
orders = [(8, 2), (1, 7), (6, 6), (2, 1), (9, 9)]
better = [(2, 1), (8, 2), (6, 6), (1, 7), (9, 9)]
fig, axes = plt.subplots(1, 2, figsize=(12, 5.6))
for ax, route, title, colour in [(axes[0], orders, "in the order received: 52 cells", RED), (axes[1], better, "nearest first: 32 cells", GREEN)]:
    ax.set_xlim(-0.5, 10); ax.set_ylim(-0.5, 10); ax.set_aspect("equal"); ax.set_xticks(range(0, 10)); ax.set_yticks(range(0, 10)); ax.grid(alpha=0.35)
    here = (0, 0)
    for stop in route:
        ax.plot([here[0], stop[0], stop[0]], [here[1], here[1], stop[1]], color=colour, lw=2.5)
        here = stop
    for i, (x, y) in enumerate(route):
        ax.plot([x], [y], "s", color=GREY, ms=14, zorder=4); ax.text(x, y, str(i + 1), ha="center", va="center", color="white", fontsize=10, weight="bold", zorder=5)
    ax.plot([0], [0], "o", color=ORANGE, mec=BLACK, ms=13, zorder=5)
    ax.set_title(title, fontsize=13)
save(fig, "fig06-warehouse.png")
print("figures saved in", os.path.abspath(OUT))
