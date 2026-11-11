# Figures for Chapter 55 - Project: measuring a room with a tape and trigonometry.
# Run:  python figures.py      (saves PNG files in ../../images/ch055/)
import math
import os
import random
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Arc, FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from heights import height_from_one_angle                      # noqa: E402
from room_survey import place_corners, shoelace_area             # noqa: E402
from survey_data import (ANGLE_ERROR_DEG, CEILING_ANGLE_DEG, CHECKS, DIAGONALS, EYE_M, SIDES,   # noqa: E402
                         TAPE_ERROR_M, WALL_DISTANCE_M)

OUT = os.path.join(HERE, "..", "..", "images", "ch055")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


C = place_corners(SIDES, DIAGONALS)

# Figure 1: the room and what we measure
fig, ax = plt.subplots(figsize=(9, 7))
ring = [C[k] for k in "ABCDE"]
ax.add_patch(Polygon(ring, closed=True, fc=L_GREY, ec=BLACK, lw=3))
for k, (x, y) in C.items():
    off = {"A": (-0.25, -0.25), "B": (0.08, -0.25), "C": (0.08, 0.05), "D": (0.0, 0.1), "E": (-0.25, 0.0)}[k]
    ax.text(x + off[0], y + off[1], k, fontsize=16, weight="bold", color=RED)
for pair, v in SIDES.items():
    (x1, y1), (x2, y2) = C[pair[0]], C[pair[1]]
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{v:.3f}", fontsize=11.5, ha="center", va="center", bbox=dict(fc="white", ec="none", pad=1))
for pair, v in DIAGONALS.items():
    (x1, y1), (x2, y2) = C[pair[0]], C[pair[1]]
    ax.plot([x1, x2], [y1, y2], color=BLUE, lw=2, ls="--")
    ax.text(0.55 * x1 + 0.45 * x2, 0.55 * y1 + 0.45 * y2, f"{v:.3f}", fontsize=11.5, color=BLUE, ha="center", bbox=dict(fc="white", ec="none", pad=1))
for pair, v in CHECKS.items():
    (x1, y1), (x2, y2) = C[pair[0]], C[pair[1]]
    ax.plot([x1, x2], [y1, y2], color=GREEN, lw=1.8, ls=":")
ax.text(2.1, -0.65, "black: walls   blue dashed: diagonals used   green dotted: extra lengths, for checking", ha="center", fontsize=11.5)
ax.set_xlim(-0.6, 4.9); ax.set_ylim(-0.9, 3.8); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-room-plan.png")

# Figure 2: three triangles fanned out from A
fig, ax = plt.subplots(figsize=(9, 7))
cols = [L_BLUE, L_GREEN, L_ORANGE]
for tri, col in zip(["ABC", "ACD", "ADE"], cols):
    ax.add_patch(Polygon([C[k] for k in tri], closed=True, fc=col, ec=BLACK, lw=1.8))
angles = []
d = 0.0
for near, far in [("B", "C"), ("C", "D"), ("D", "E")]:
    a1 = math.degrees(math.atan2(C[near][1], C[near][0])); a2 = math.degrees(math.atan2(C[far][1], C[far][0]))
    angles.append((a1, a2))
for (a1, a2), r, col in zip(angles, [0.9, 1.1, 1.3], [BLUE, GREEN, ORANGE]):
    ax.add_patch(Arc((0, 0), 2 * r, 2 * r, theta1=a1, theta2=a2, color=col, lw=3))
ax.text(1.0, 0.2, "1", fontsize=14, color=BLUE, weight="bold"); ax.text(0.75, 0.95, "2", fontsize=14, color=GREEN, weight="bold")
ax.text(0.3, 1.35, "3", fontsize=14, color=ORANGE, weight="bold")
for k, (x, y) in C.items():
    ax.plot([x], [y], "o", color=RED, ms=9); ax.text(x + 0.08, y + 0.08, k, fontsize=15, weight="bold", color=RED)
ax.text(2.2, -0.55, "each angle at A comes from the law of cosines; adding them turns the plan round A", ha="center", fontsize=11.5)
ax.set_xlim(-0.4, 4.8); ax.set_ylim(-0.8, 3.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-fan.png")

# Figure 3: ceiling height side view
fig, ax = plt.subplots(figsize=(9, 5.5))
ceil = height_from_one_angle(EYE_M, WALL_DISTANCE_M, CEILING_ANGLE_DEG)
ax.plot([-0.5, 3.6], [0, 0], color=BLACK, lw=2); ax.plot([3.0, 3.0], [0, ceil + 0.3], color=GREY, lw=6)
ax.plot([-0.5, 3.0], [ceil, ceil], color=GREY, lw=4); ax.text(-0.4, ceil + 0.08, "ceiling", fontsize=12)
ax.add_patch(Rectangle((-0.05, 0), 0.1, EYE_M, fc=ORANGE, ec=BLACK)); ax.text(-0.45, EYE_M / 2, "phone at\n1.20 m", fontsize=11.5, ha="right", va="center")
ax.plot([0, 3.0], [EYE_M, EYE_M], color=GREEN, lw=2, ls="--"); ax.text(1.5, EYE_M - 0.18, "3.00 m to the wall", ha="center", fontsize=12, color=GREEN)
ax.plot([0, 3.0], [EYE_M, ceil], color=RED, lw=2.5)
ax.add_patch(Arc((0, EYE_M), 1.2, 1.2, theta1=0, theta2=CEILING_ANGLE_DEG, color=RED, lw=2)); ax.text(0.7, EYE_M + 0.12, "30.3", fontsize=12, color=RED)
ax.annotate("", xy=(3.2, ceil), xytext=(3.2, EYE_M), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=2))
ax.text(3.28, (ceil + EYE_M) / 2, "3.00 x tan 30.3\n= 1.753 m", fontsize=12, color=BLUE, va="center")
ax.set_xlim(-1.3, 4.6); ax.set_ylim(-0.2, 3.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-ceiling.png")

# Figure 4: the two-angle method
fig, ax = plt.subplots(figsize=(10, 5.2))
h_above = 2.935 - 1.2
d2 = 2.221
ax.plot([-2.0, 2.8], [0, 0], color=BLACK, lw=2)
sx = d2
ax.plot([sx, sx], [0, 2.935], color=GREY, lw=5); ax.text(sx + 0.08, 2.9, "shelf top", fontsize=12)
ax.add_patch(Rectangle((sx - 0.9, 0), 0.8, 0.75, fc=L_GREY, ec=BLACK)); ax.text(sx - 0.5, 0.35, "table", ha="center", fontsize=11)
for x0, ang, lab, col in [(-1.5, 25.0, "spot 1: 25.0", BLUE), (0.0, 38.0, "spot 2: 38.0", GREEN)]:
    ax.plot([x0, x0], [0, 1.2], color=ORANGE, lw=4)
    ax.plot([x0, sx], [1.2, 2.935], color=col, lw=2.2)
    ax.add_patch(Arc((x0, 1.2), 1.0, 1.0, theta1=0, theta2=ang, color=col, lw=2)); ax.text(x0 + 0.55, 1.28, lab, fontsize=11.5, color=col)
ax.plot([-1.5, sx], [1.2, 1.2], color=GREY, ls=":", lw=1.5)
ax.annotate("", xy=(0, -0.25), xytext=(-1.5, -0.25), arrowprops=dict(arrowstyle="<->", lw=1.8)); ax.text(-0.75, -0.5, "1.50 m (measured)", ha="center", fontsize=11.5)
ax.annotate("", xy=(sx, -0.25), xytext=(0, -0.25), arrowprops=dict(arrowstyle="<->", lw=1.8, color=RED)); ax.text(sx / 2, -0.5, "2.221 m (found)", ha="center", fontsize=11.5, color=RED)
ax.set_xlim(-2.1, 3.6); ax.set_ylim(-0.7, 3.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-two-angles.png")

# Figure 5: Monte Carlo spreads
random.seed(55)


def jitter(lengths):
    return {k: v + random.gauss(0, TAPE_ERROR_M) for k, v in lengths.items()}


areas, ceilings = [], []
for _ in range(10_000):
    cc = place_corners(jitter(SIDES), jitter(DIAGONALS))
    areas.append(shoelace_area([cc[k] for k in "ABCDE"]))
    ceilings.append(height_from_one_angle(EYE_M + random.gauss(0, TAPE_ERROR_M), WALL_DISTANCE_M + random.gauss(0, TAPE_ERROR_M),
                                          CEILING_ANGLE_DEG + random.gauss(0, ANGLE_ERROR_DEG)))
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
axes[0].hist(areas, bins=50, color=L_BLUE, edgecolor=BLUE); axes[0].set_xlabel("floor area (m^2)"); axes[0].set_title("area: spread 0.025 m^2 (0.19%)", fontsize=12.5)
axes[1].hist(ceilings, bins=50, color=L_GREEN, edgecolor=GREEN); axes[1].set_xlabel("ceiling height (m)"); axes[1].set_title("ceiling: spread 0.036 m (1.2%)", fontsize=12.5)
for ax in axes:
    ax.set_ylabel("number of runs (of 10,000)"); ax.grid(alpha=0.3)
save(fig, "fig05-monte-carlo.png")

# Figure 6: grid map
grid_text = []
import io, contextlib, runpy  # noqa: E401,E402
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    runpy.run_path(os.path.join(HERE, "room_map.py"), run_name="__main__")
rows = [r for r in buf.getvalue().splitlines() if r.startswith("#")]
fig, ax = plt.subplots(figsize=(8, 7))
for r, line in enumerate(rows):
    for c, ch in enumerate(line):
        y = len(rows) - 1 - r
        ax.add_patch(Rectangle((c, y), 1, 1, fc=(GREY if ch == "#" else "white"), ec=L_GREY, lw=0.5))
scale = 1 / 0.25
poly = [((x * scale) + 1, (y * scale) + 1) for x, y in ring]
ax.add_patch(Polygon(poly, closed=True, fill=False, ec=RED, lw=2.5))
ax.text(len(rows[0]) / 2, -1.0, "grey: wall or outside    white: free floor    red: the measured walls", ha="center", fontsize=11.5)
ax.set_xlim(-0.2, len(rows[0]) + 0.2); ax.set_ylim(-1.6, len(rows) + 0.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-grid-map.png")

# Figure 7: the chapters that the project uses
fig, ax = plt.subplots(figsize=(13, 5.6))
boxes = [("units, measuring,\nuncertainty\n(Ch 39, 54)", 0.0, 3.0, L_GREY), ("law of cosines\n(Ch 51)", 3.3, 3.0, L_BLUE),
         ("radians, cos, sin\nx = r cos t\n(Ch 47, 49, 50)", 6.6, 3.0, L_BLUE), ("corners (x, y)\n(Ch 42)", 9.9, 3.0, L_GREEN),
         ("tan for heights\nlaw of sines idea\n(Ch 49, 51)", 0.0, 0.3, L_BLUE), ("area: triangles\nand shoelace sum\n(Ch 48, 51, 53)", 3.3, 0.3, L_ORANGE),
         ("Monte Carlo error\nmean and spread\n(Ch 31, 53, 54)", 6.6, 0.3, L_ORANGE), ("grid map for\nGridBot and Rover\n(Ch 36, 42)", 9.9, 0.3, L_GREEN)]
for text, x, y, col in boxes:
    ax.add_patch(FancyBboxPatch((x, y), 2.8, 1.9, boxstyle="round,pad=0.02,rounding_size=0.12", fc=col, ec=BLACK))
    ax.text(x + 1.4, y + 0.95, text, ha="center", va="center", fontsize=11.5)
for x in (2.8, 6.1, 9.4):
    arrow(ax, (x + 0.02, 3.95), (x + 0.48, 3.95))
arrow(ax, (11.3, 2.95), (11.3, 2.25))
ax.set_xlim(-0.2, 12.9); ax.set_ylim(0.0, 5.2); ax.axis("off")
save(fig, "fig07-part3-map.png")
print("figures saved in", os.path.abspath(OUT))
