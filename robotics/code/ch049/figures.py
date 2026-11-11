# Figures for Chapter 49 - Trigonometry part 1: sin, cos, tan in right triangles.
# Run:  python figures.py      (saves PNG files in ../../images/ch049/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Arc, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch049")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


# Figure 1: names of the sides
fig, ax = plt.subplots(figsize=(9, 5.2))
A, B, C = (0, 0), (5, 0), (5, 3)
ax.add_patch(Polygon([A, B, C], closed=True, fc=L_BLUE, ec=BLACK, lw=2))
ax.add_patch(Rectangle((4.7, 0), 0.3, 0.3, fill=False, ec=BLACK, lw=1.5))
ax.add_patch(Arc(A, 1.6, 1.6, theta1=0, theta2=math.degrees(math.atan2(3, 5)), color=RED, lw=3))
ax.text(0.95, 0.2, "angle", fontsize=13, color=RED)
ax.text(2.5, -0.4, "adjacent: next to the angle", ha="center", fontsize=13, color=GREEN, weight="bold")
ax.text(5.15, 1.5, "opposite:\nacross from\nthe angle", fontsize=13, color=BLUE, weight="bold", va="center")
ax.text(2.0, 1.75, "hypotenuse:\nthe longest side", fontsize=13, color=ORANGE, weight="bold", ha="right", rotation=0)
ax.plot([0, 5], [0, 0], color=GREEN, lw=5); ax.plot([5, 5], [0, 3], color=BLUE, lw=5); ax.plot([0, 5], [0, 3], color=ORANGE, lw=5)
ax.set_xlim(-1, 7.2); ax.set_ylim(-0.8, 3.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-side-names.png")

# Figure 2: similar triangles
fig, ax = plt.subplots(figsize=(10, 4.6))
t = math.radians(30)
for h, col in [(2, L_ORANGE), (4, L_GREEN), (6, L_BLUE)]:
    ax.add_patch(Polygon([(0, 0), (h * math.cos(t), 0), (h * math.cos(t), h * math.sin(t))], closed=True, fc=col, ec=BLACK, lw=1.5, alpha=0.9))
    ax.text(h * math.cos(t) + 0.08, h * math.sin(t) / 2, f"opp {h * 0.5:g}\nhyp {h}", fontsize=11.5, va="center")
ax.add_patch(Arc((0, 0), 1.4, 1.4, theta1=0, theta2=30, color=RED, lw=3)); ax.text(0.8, 0.12, "30", fontsize=12, color=RED)
ax.text(2.8, 3.4, "opp / hyp = 0.5 for all three: that number is sin 30", fontsize=13, ha="center")
ax.set_xlim(-0.2, 6.3); ax.set_ylim(-0.2, 3.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-similar.png")

# Figure 3: the two special triangles
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ax = axes[0]
ax.add_patch(Polygon([(0, 0), (2, 0), (2, 2)], closed=True, fc=L_GREEN, ec=BLACK, lw=2))
ax.text(1, -0.3, "1", ha="center", fontsize=15); ax.text(2.15, 1, "1", fontsize=15); ax.text(0.75, 1.15, "square root of 2", fontsize=12.5, rotation=45, ha="center")
ax.text(0.5, 0.12, "45", fontsize=13, color=RED); ax.text(1.8, 1.55, "45", fontsize=13, color=RED)
ax.set_title("half a square: sin 45 = cos 45 = 1/1.414 = 0.707", fontsize=12.5)
ax.set_xlim(-0.3, 3.0); ax.set_ylim(-0.6, 2.4); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
s3 = math.sqrt(3)
ax.add_patch(Polygon([(0, 0), (2, 0), (1, s3)], closed=True, fc=L_GREY, ec=GREY, lw=1.5, ls="--"))
ax.add_patch(Polygon([(0, 0), (1, 0), (1, s3)], closed=True, fc=L_BLUE, ec=BLACK, lw=2))
ax.text(0.5, -0.3, "1", ha="center", fontsize=15); ax.text(0.25, 1.0, "2", fontsize=15); ax.text(1.05, 0.7, "1.732", fontsize=12.5)
ax.text(0.33, 0.12, "60", fontsize=13, color=RED); ax.text(0.85, 1.3, "30", fontsize=13, color=RED)
ax.set_title("half an equilateral triangle: sin 30 = 1/2", fontsize=12.5)
ax.set_xlim(-0.3, 2.4); ax.set_ylim(-0.6, 2.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-special.png")

# Figure 4: a beam at an angle -> x and y
fig, ax = plt.subplots(figsize=(8, 6))
r, deg = 3.0, 35
t = math.radians(deg)
x, y = r * math.cos(t), r * math.sin(t)
ax.add_patch(Rectangle((-0.35, -0.25), 0.5, 0.5, fc=ORANGE, ec=BLACK, zorder=5))
arrow(ax, (0, 0), (x, y), RED, 3)
ax.plot([0, x], [0, 0], color=GREEN, lw=4); ax.plot([x, x], [0, y], color=BLUE, lw=4)
ax.plot([x], [y], "o", color=BLACK, ms=10, zorder=6)
ax.text(1.0, 1.15, "range r = 3.0 m", rotation=deg, fontsize=13, color=RED)
ax.text(x / 2, -0.35, f"x = r cos 35 = {x:.2f} m", ha="center", fontsize=13, color=GREEN)
ax.text(x + 0.1, y / 2, f"y = r sin 35\n  = {y:.2f} m", fontsize=13, color=BLUE)
ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=deg, color=BLACK, lw=2)); ax.text(0.7, 0.12, "35", fontsize=12)
ax.set_xlim(-0.6, 4.2); ax.set_ylim(-0.7, 2.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-polar-to-xy.png")

# Figure 5: rotating a shape
shape = [(0, 0), (2, 0), (2, 1), (0, 1)]
def rot(p, d):
    t = math.radians(d); c, s = math.cos(t), math.sin(t)
    return [(px * c - py * s, px * s + py * c) for px, py in p]
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.6))
ax = axes[0]
for d, col, lab in [(0, ORANGE, "x direction (1, 0)"), (90, GREEN, "y direction (0, 1)")]:
    pass
t = math.radians(30)
arrow(ax, (0, 0), (1, 0), GREY, 2); arrow(ax, (0, 0), (0, 1), GREY, 2)
arrow(ax, (0, 0), (math.cos(t), math.sin(t)), RED, 3); arrow(ax, (0, 0), (-math.sin(t), math.cos(t)), BLUE, 3)
ax.text(1.0, -0.15, "(1, 0)", fontsize=12, color="#555555"); ax.text(0.05, 1.05, "(0, 1)", fontsize=12, color="#555555")
ax.text(0.9, 0.55, "(cos, sin)", fontsize=13, color=RED); ax.text(-1.05, 0.95, "(-sin, cos)", fontsize=13, color=BLUE)
ax.set_title("turn both directions by 30 degrees", fontsize=13)
ax.set_xlim(-1.2, 1.5); ax.set_ylim(-0.4, 1.3); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
ax.axhline(0, color=BLACK, lw=1); ax.axvline(0, color=BLACK, lw=1); ax.grid(alpha=0.3)
ax.add_patch(Polygon(shape, closed=True, fc=ORANGE, ec=BLACK, alpha=0.85, label="start"))
ax.add_patch(Polygon(rot(shape, 30), closed=True, fc=L_BLUE, ec=BLUE, lw=2, label="turned 30"))
ax.add_patch(Polygon(rot(shape, 90), closed=True, fc=L_GREEN, ec=GREEN, lw=2, hatch="//", label="turned 90"))
ax.set_xlim(-1.5, 2.5); ax.set_ylim(-0.5, 2.5); ax.set_aspect("equal"); ax.legend(loc="upper right", fontsize=11)
ax.set_title("the rectangle from Chapter 42, turned about the origin", fontsize=12.5)
save(fig, "fig05-rotation.png")

# Figure 6: laser scan
readings = [(-60, 2.31), (-30, 1.73), (0, 1.50), (30, 1.73), (60, 3.00)]
fig, ax = plt.subplots(figsize=(8, 7))
ax.add_patch(Rectangle((-0.2, -0.15), 0.3, 0.3, fc=ORANGE, ec=BLACK, zorder=5))
for d, r in readings:
    t = math.radians(d)
    ax.plot([0, r * math.cos(t)], [0, r * math.sin(t)], color=RED, lw=1.2, ls=":")
    ax.plot([r * math.cos(t)], [r * math.sin(t)], "o", color=BLUE, ms=11, zorder=6)
    ax.text(r * math.cos(t) + 0.08, r * math.sin(t) + 0.08, f"{d} deg, {r} m", fontsize=11)
ax.plot([1.5, 1.5], [-2.8, 2.9], color=GREY, lw=8, alpha=0.6); ax.text(1.62, -2.75, "wall", fontsize=12)
ax.add_patch(Rectangle((1.0, -2.25), 0.25, 0.5, fc=GREY, ec=BLACK)); ax.text(0.45, -2.6, "box", fontsize=12)
ax.set_xlabel("x: forward (m)"); ax.set_ylabel("y: left (m)"); ax.grid(alpha=0.3)
ax.set_xlim(-0.5, 3.0); ax.set_ylim(-3.0, 3.1); ax.set_aspect("equal")
save(fig, "fig06-scan.png")

# Figure 7: forces on a ramp
fig, ax = plt.subplots(figsize=(9, 5))
th = math.atan(0.25)
L = 6
ax.add_patch(Polygon([(0, 0), (L, 0), (L, L * math.tan(th))], closed=True, fc=L_GREY, ec=BLACK))
cx, cy = 3.2, 3.2 * math.tan(th)
c, s = math.cos(th), math.sin(th)
body = [(cx - 0.4 * c - 0 * s, cy - 0.4 * s), (cx + 0.4 * c, cy + 0.4 * s), (cx + 0.4 * c - 0.4 * s, cy + 0.4 * s + 0.4 * c), (cx - 0.4 * c - 0.4 * s, cy - 0.4 * s + 0.4 * c)]
ax.add_patch(Polygon(body, closed=True, fc=ORANGE, ec=BLACK, zorder=5))
mx, my = cx - 0.2 * s, cy + 0.2 * c
arrow(ax, (mx, my), (mx, my - 1.6), BLACK, 3); ax.text(mx + 0.1, my - 1.5, "weight m g", fontsize=12.5)
arrow(ax, (mx, my), (mx - 1.4 * c, my - 1.4 * s), RED, 3)
ax.text(mx - 3.3, my + 0.15, "m g sin(angle):\npulls it down the ramp", fontsize=12, color=RED)
ax.add_patch(Arc((0, 0), 2.2, 2.2, theta1=0, theta2=math.degrees(th), color=BLUE, lw=2.5)); ax.text(1.2, 0.08, "angle", fontsize=12, color=BLUE)
ax.set_xlim(-0.3, 6.5); ax.set_ylim(-1.0, 2.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig07-ramp.png")
print("figures saved in", os.path.abspath(OUT))
