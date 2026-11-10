# Figures for Chapter 26 — Modules and the math module.
# Run:  python figures.py      (saves PNG files in ../../images/ch026/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Wedge

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch026")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


def filebox(ax, x, y, w, h, title, lines, face):
    ax.add_patch(Rectangle((x, y), w, h, fc=face, ec=BLACK, lw=1.4))
    ax.add_patch(Rectangle((x, y + h - 0.5), w, 0.5, fc="white", ec=BLACK, lw=1.2))
    ax.text(x + 0.15, y + h - 0.25, title, va="center", fontsize=12, family=MONO, weight="bold")
    for i, t in enumerate(lines):
        ax.text(x + 0.2, y + h - 0.9 - i * 0.42, t, va="center", fontsize=11, family=MONO)


# ---------- Figure 1: one module, many programs ----------
fig, ax = plt.subplots(figsize=(13.5, 5.6))
filebox(ax, 0.3, 1.3, 4.8, 3.3, "rover_math.py", ["def clamp(...):", "def ticks_to_metres(...):", "def heading_error(...):", "def move(...):"], L_GREEN)
filebox(ax, 7.7, 3.3, 5.3, 1.7, "drive_any_way.py", ["import rover_math", "rover_math.move(...)"], L_BLUE)
filebox(ax, 7.7, 0.7, 5.3, 1.7, "go_to_goal.py", ["from rover_math import heading_error", "heading_error(...)"], L_ORANGE)
arrow(ax, (5.2, 3.3), (7.6, 4.1), GREEN, 3); arrow(ax, (5.2, 2.6), (7.6, 1.6), GREEN, 3)
ax.text(2.7, 0.7, "written once, tested once", ha="center", fontsize=13, weight="bold", color=GREEN)
ax.text(6.4, 3.0, "import", ha="center", fontsize=13, weight="bold", color=GREEN)
ax.set_xlim(0, 13.2); ax.set_ylim(0.4, 5.3); ax.axis("off")
save(fig, "fig01-one-module-many-programs.png")

# ---------- Figure 2: degrees and radians ----------
fig, ax = plt.subplots(figsize=(8.5, 8.0))
ax.add_patch(Circle((0, 0), 1.0, fc="white", ec=BLACK, lw=2))
for d, lab in [(0, "0"), (90, "pi/2"), (180, "pi"), (270, "3 pi/2")]:
    a = math.radians(d)
    ax.plot([0, math.cos(a)], [0, math.sin(a)], color=L_GREY, lw=1.2)
    ax.text(1.27 * math.cos(a), 1.2 * math.sin(a), f"{d} deg\n{lab} rad", ha="center", va="center", fontsize=12, weight="bold")
a = 1.0
ax.add_patch(Wedge((0, 0), 1.0, 0, math.degrees(a), fc=L_ORANGE, ec=BLACK))
ax.plot([0, 1], [0, 0], color=BLUE, lw=3); ax.plot([0, math.cos(a)], [0, math.sin(a)], color=BLUE, lw=3)
ax.text(0.5, -0.09, "radius r", color=BLUE, ha="center", fontsize=12, weight="bold")
ax.text(1.14, 0.56, "arc as long\nas the radius", color=ORANGE, fontsize=12, weight="bold", ha="left", va="center")
ax.text(0.35, 0.16, "1 radian\n= 57.3 deg", ha="center", fontsize=11.5, weight="bold")
ax.text(0, -1.55, "degrees x pi / 180 = radians", ha="center", fontsize=14, family=MONO, weight="bold")
ax.set_xlim(-1.7, 1.9); ax.set_ylim(-1.75, 1.45); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-degrees-and-radians.png")

# ---------- Figure 3: a compass heading splits into east and north ----------
fig, ax = plt.subplots(figsize=(9.5, 7.2))
H, D = 30, 4.0
h = math.radians(H)
ex, ny = D * math.sin(h), D * math.cos(h)
ax.annotate("", xy=(0, 4.6), xytext=(0, -0.2), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.5))
ax.annotate("", xy=(3.4, 0), xytext=(-0.5, 0), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.5))
ax.text(0.0, 4.75, "north (y)", ha="center", fontsize=12.5, color=GREY); ax.text(3.45, 0, "east (x)", va="center", fontsize=12.5, color=GREY)
arrow(ax, (0, 0), (ex, ny), BLUE, 4)
ax.plot([ex, ex], [0, ny], color=RED, lw=3, ls="--"); ax.plot([0, ex], [ny, ny], color=GREEN, lw=3, ls="--")
ax.add_patch(Wedge((0, 0), 1.3, 90 - H, 90, fc=L_ORANGE, ec=ORANGE))
ax.annotate("heading", xy=(0.2, 1.1), xytext=(-0.75, 1.5), fontsize=12.5, color=ORANGE, weight="bold", arrowprops=dict(arrowstyle="-|>", color=ORANGE))
ax.text(ex / 2 + 0.33, ny / 2 - 0.2, "distance", color=BLUE, fontsize=13, weight="bold", rotation=60, ha="center", va="center")
ax.text(ex / 2, ny + 0.2, "east = distance x sin(heading)", ha="center", color=GREEN, fontsize=12.5, weight="bold")
ax.text(ex + 0.12, ny / 2, "north = distance\nx cos(heading)", color=RED, fontsize=12.5, weight="bold", va="center")
ax.set_xlim(-0.8, 4.6); ax.set_ylim(-0.4, 5.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-heading-components.png")

# ---------- Figure 4: the path ----------
legs = [(90, 2.0), (45, 1.0), (0, 0.5), (200, 1.5)]
pts = [(0.0, 0.0)]
for hd, d in legs:
    x, y = pts[-1]
    pts.append((x + d * math.sin(math.radians(hd)), y + d * math.cos(math.radians(hd))))
fig, ax = plt.subplots(figsize=(10.5, 6.2))
for i in range(len(legs)):
    ax.add_patch(FancyArrowPatch(pts[i], pts[i + 1], arrowstyle="-|>", mutation_scale=18, color=BLUE, lw=3, zorder=2))
    mx, my = (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2
    offs = [(0, -0.2), (0.75, -0.22), (0.5, 0), (-0.6, 0.05)][i]
    ax.text(mx + offs[0], my + offs[1], f"{legs[i][0]} deg, {legs[i][1]} m", fontsize=12, ha="center", weight="bold", color=BLUE)
ax.plot(0, 0, "s", color=ORANGE, ms=14, mec=BLACK, zorder=3)
ax.plot(*pts[-1], "*", color=ORANGE, ms=24, mec=BLACK, zorder=3)
ax.text(pts[-1][0] - 0.1, pts[-1][1] - 0.32, "ends at (2.194, -0.202)", ha="center", fontsize=12)
ax.grid(alpha=0.3); ax.set_xlabel("x, east (m)"); ax.set_ylabel("y, north (m)"); ax.set_aspect("equal")
ax.set_xlim(-0.5, 3.8); ax.set_ylim(-0.8, 1.6)
save(fig, "fig04-any-direction-path.png")

# ---------- Figure 5: bearing to a goal ----------
fig, ax = plt.subplots(figsize=(9.5, 7.6))
rx, ry = 1.0, 1.0
gx, gy = 3.0, 4.0
for g in range(0, 6):
    ax.plot([g, g], [0, 5], color=L_GREY, lw=1, zorder=0); ax.plot([0, 5], [g, g], color=L_GREY, lw=1, zorder=0)
ax.plot(rx, ry, "s", color=ORANGE, ms=18, mec=BLACK, zorder=4)
ax.plot(gx, gy, "*", color=GREEN, ms=26, mec=BLACK, zorder=4)
ax.text(gx + 0.2, gy + 0.1, "goal (3, 4)", fontsize=13, weight="bold")
ax.text(rx - 0.15, ry - 0.42, "Rover (1, 1)", fontsize=13, weight="bold", ha="center")
ax.add_patch(FancyArrowPatch((rx, ry), (rx + 1.9, ry), arrowstyle="-|>", mutation_scale=18, color=BLUE, lw=3, zorder=3))
ax.text(rx + 1.95, ry - 0.3, "facing 90 (east)", fontsize=12, color=BLUE, weight="bold", ha="center")
ax.plot([rx, rx], [ry, 4.3], color=GREY, ls="--", lw=1.5, zorder=1); ax.text(rx - 0.05, 4.4, "north", fontsize=12, color=GREY, ha="center")
ax.add_patch(FancyArrowPatch((rx, ry), (gx, gy), arrowstyle="-|>", mutation_scale=18, color=RED, lw=3, zorder=2))
ax.add_patch(Wedge((rx, ry), 1.0, 90 - 33.7, 90, fc=L_ORANGE, ec=ORANGE, zorder=1))
ax.text(rx + 0.25, ry + 1.2, "33.7", fontsize=12, color=ORANGE, weight="bold")
ax.add_patch(Wedge((rx, ry), 0.6, 0, 90 - 33.7, fc=L_RED, ec=RED, zorder=1))
ax.text(rx + 0.68, ry + 0.25, "turn left\n56.3", fontsize=11.5, color=RED, weight="bold")
ax.text(gx - 1.4, gy - 1.35, "3.606 m", fontsize=13, color=RED, weight="bold", rotation=56)
ax.set_xlim(-0.2, 5.1); ax.set_ylim(-0.2, 5.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-bearing-to-a-goal.png")
print("figures saved in", os.path.abspath(OUT))
