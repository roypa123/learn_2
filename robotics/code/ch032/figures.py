# Figures for Chapter 32 — Drawing with turtle: a robot on the screen.
# turtle cannot save a PNG by itself, so these figures redraw the same paths with matplotlib.
# Run:  python figures.py      (saves PNG files in ../../images/ch032/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch032")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.5):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, zorder=3))


def turtle_mark(ax, x, y, deg, colour=ORANGE, s=0.22):
    # deg is a maths angle: 0 = pointing right
    a = math.radians(deg)
    fx, fy = math.cos(a), math.sin(a)
    sx, sy = -fy, fx
    ax.add_patch(Polygon([(x + fx * s, y + fy * s), (x - fx * s + sx * s * 0.7, y - fy * s + sy * s * 0.7),
                          (x - fx * s - sx * s * 0.7, y - fy * s - sy * s * 0.7)], closed=True, fc=colour, ec=BLACK, zorder=4))


# ---------- Figure 1: drawing a square step by step ----------
fig, axes = plt.subplots(1, 4, figsize=(14.5, 4.4))
steps = [("forward(100)", [(0, 0), (1, 0)], 0), ("left(90)", [(0, 0), (1, 0)], 90),
         ("forward(100)", [(0, 0), (1, 0), (1, 1)], 90), ("repeat 4 times", [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], 0)]
for ax, (t, pts, h) in zip(axes, steps):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=BLUE, lw=3)
    turtle_mark(ax, pts[-1][0], pts[-1][1], h)
    ax.set_title(t, family=MONO, fontsize=13, weight="bold")
    ax.set_xlim(-0.45, 1.45); ax.set_ylim(-0.45, 1.45); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-drawing-a-square.png")

# ---------- Figure 2: the two heading systems ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 6.0))
for ax, title, labels in [(axes[0], 'mode "standard" (the default)', [("0", 0), ("90", 90), ("180", 180), ("270", 270)]),
                          (axes[1], 'mode "logo": a compass', [("90", 0), ("0", 90), ("270", 180), ("180", 270)])]:
    ax.add_patch(plt.Circle((0, 0), 1, fc="white", ec=BLACK, lw=2))
    for lab, d in labels:
        a = math.radians(d)
        arrow(ax, (0, 0), (0.92 * math.cos(a), 0.92 * math.sin(a)), GREY, 1.8)
        ax.text(1.2 * math.cos(a), 1.2 * math.sin(a), lab, ha="center", va="center", fontsize=15, weight="bold", family=MONO)
    ax.set_title(title, fontsize=14, weight="bold", family=MONO)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect("equal"); ax.axis("off")
axes[0].text(0, -1.42, "0 points right. Angles grow counter-clockwise.", ha="center", fontsize=12)
axes[1].text(0, -1.42, "0 points up (north). Angles grow clockwise.", ha="center", fontsize=12)
save(fig, "fig02-two-heading-systems.png")

# ---------- Figure 3: the route window ----------
route = "FFRFFLFRFF"
x, y, h = 0, 0, 0
pts = [(0, 0)]
for L in route:
    if L == "L":
        h = (h - 1) % 4
    elif L == "R":
        h = (h + 1) % 4
    else:
        dx, dy = [(0, 1), (1, 0), (0, -1), (-1, 0)][h]
        x += dx; y += dy
        pts.append((x, y))
fig, ax = plt.subplots(figsize=(9, 6.2))
ax.add_patch(Rectangle((-2.2, -1.3), 9.2, 5.6, fc="white", ec=BLACK, lw=2))
ax.add_patch(Rectangle((-2.2, 4.3), 9.2, 0.42, fc=L_GREY, ec=BLACK, lw=2))
ax.text(-2.05, 4.5, "Rover route", va="center", fontsize=11.5)
ax.plot([p[0] for p in pts], [p[1] for p in pts], color=ORANGE, lw=4)
turtle_mark(ax, pts[-1][0], pts[-1][1], 0, ORANGE, 0.28)
ax.plot(0, 0, "o", color=GREY, ms=8, zorder=5)
ax.text(0.15, -0.3, "(0, 0): the centre of the window", fontsize=11.5)
ax.text(4.3, 3.25, "(240, 180) px\n= (4.0, 3.0) m", fontsize=11.5, ha="left", va="center")
ax.set_xlim(-2.4, 7.2); ax.set_ylim(-1.5, 4.9); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-route-window.png")

# ---------- Figure 4: the lawnmower path ----------
W, H, R = 8.0, 4.0, 0.5
fig, ax = plt.subplots(figsize=(11.5, 6.2))
ax.add_patch(Rectangle((0, 0), W, H, fc="white", ec=BLACK, lw=3))
xs, ys = [R / 2], [0.1]
for i in range(int(W / R)):
    ye = H - 0.1 if i % 2 == 0 else 0.1
    x_m = R / 2 + i * R
    xs.append(x_m); ys.append(ye)
    if i < int(W / R) - 1:
        xs.append(x_m + R); ys.append(ye)
ax.plot(xs, ys, color=BLUE, lw=2.5)
ax.annotate("", xy=(0.25, -0.2), xytext=(0.75, -0.2), arrowprops=dict(arrowstyle="<->", color=RED, lw=2))
ax.text(0.9, -0.28, "strip width 0.5 m", fontsize=12, color=RED, va="center")
ax.text(4.0, 4.3, "8 m x 4 m room: 16 passes, 68.3 m of driving", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-0.4, 8.4); ax.set_ylim(-0.6, 4.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-lawnmower-path.png")

# ---------- Figure 5: arm poses ----------
L1, L2 = 0.3, 0.2
fig, ax = plt.subplots(figsize=(10.5, 6.6))
ax.axhline(0, color=L_GREY, lw=1.5, zorder=0); ax.axvline(0, color=L_GREY, lw=1.5, zorder=0)
for s, e, c in [(30, 45, BLUE), (60, -30, GREEN), (100, 60, RED)]:
    a, b = math.radians(s), math.radians(s + e)
    ex, ey = L1 * math.cos(a), L1 * math.sin(a)
    tx, ty = ex + L2 * math.cos(b), ey + L2 * math.sin(b)
    ax.plot([0, ex, tx], [0, ey, ty], color=c, lw=5, solid_capstyle="round", label=f"shoulder {s}, elbow {e}: tip ({tx:.3f}, {ty:.3f})")
    ax.plot(ex, ey, "o", color=c, ms=11, mec=BLACK, zorder=4); ax.plot(tx, ty, "o", color=c, ms=15, mec=BLACK, zorder=4)
ax.plot(0, 0, "s", color=GREY, ms=16, mec=BLACK, zorder=5)
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.legend(loc="lower left", framealpha=1, fontsize=11); ax.set_xlim(-0.35, 0.45); ax.set_ylim(-0.17, 0.5)
save(fig, "fig05-arm-poses.png")
print("figures saved in", os.path.abspath(OUT))
