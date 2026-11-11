# Figures for Chapter 48 - Geometry: triangles, Pythagoras, circles.
# Run:  python figures.py      (saves PNG files in ../../images/ch048/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Circle, Wedge, Rectangle, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch048")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: angles of a triangle add to 180
fig, ax = plt.subplots(figsize=(9, 5))
A, B, C = (0, 0), (6, 0), (2, 3.2)
ax.add_patch(Polygon([A, B, C], closed=True, fc=L_BLUE, ec=BLACK, lw=2))
ax.plot([-1.5, 7], [3.2, 3.2], color=GREY, ls="--", lw=2)
ax.text(6.0, 3.35, "line through the top, parallel to the bottom", fontsize=11.5, color="#555555", ha="right")
angA = math.degrees(math.atan2(3.2, 2)); angB = math.degrees(math.atan2(3.2, -4))
ax.add_patch(Arc(A, 1.2, 1.2, theta1=0, theta2=angA, color=RED, lw=3)); ax.text(0.75, 0.3, "a", fontsize=15, color=RED)
ax.add_patch(Arc(B, 1.2, 1.2, theta1=angB, theta2=180, color=GREEN, lw=3)); ax.text(5.0, 0.25, "b", fontsize=15, color=GREEN)
ax.add_patch(Arc(C, 1.2, 1.2, theta1=angA + 180, theta2=angB + 180, color=ORANGE, lw=3)); ax.text(1.95, 2.05, "c", fontsize=15, color=ORANGE)
ax.add_patch(Arc(C, 1.2, 1.2, theta1=180, theta2=angA + 180, color=RED, lw=3)); ax.text(1.1, 2.9, "a", fontsize=15, color=RED)
ax.add_patch(Arc(C, 1.2, 1.2, theta1=angB + 180, theta2=360, color=GREEN, lw=3)); ax.text(2.85, 2.9, "b", fontsize=15, color=GREEN)
ax.text(3.0, -0.6, "along the dashed line: a + c + b = a straight line = 180 degrees", ha="center", fontsize=12.5)
ax.set_xlim(-1.6, 7.2); ax.set_ylim(-0.9, 3.8); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-triangle-180.png")

# Figure 2: squares on the sides of a 3-4-5 triangle
fig, ax = plt.subplots(figsize=(8, 8))
P, Q, R = (0, 0), (4, 0), (0, 3)
ax.add_patch(Polygon([P, Q, R], closed=True, fc=ORANGE, ec=BLACK, lw=2))
for i in range(4):
    for j in range(4):
        ax.add_patch(Rectangle((i, -4 + j), 1, 1, fc=L_BLUE, ec=BLUE))
for i in range(3):
    for j in range(3):
        ax.add_patch(Rectangle((-3 + i, j), 1, 1, fc=L_GREEN, ec=GREEN))
ax.add_patch(Polygon([(4, 0), (0, 3), (3, 7), (7, 4)], closed=True, fc=L_RED, ec=RED, lw=2))
ax.text(2, -2, "4 x 4 = 16", ha="center", fontsize=15, weight="bold")
ax.text(-1.5, 1.5, "3 x 3\n= 9", ha="center", va="center", fontsize=15, weight="bold")
ax.text(3.5, 3.6, "5 x 5 = 25", ha="center", fontsize=15, weight="bold")
ax.text(1.1, 0.7, "right\nangle", fontsize=10.5)
ax.add_patch(Rectangle((0, 0), 0.35, 0.35, fill=False, ec=BLACK, lw=1.5))
ax.text(2.0, -4.8, "9 + 16 = 25", ha="center", fontsize=16, weight="bold")
ax.set_xlim(-3.5, 7.5); ax.set_ylim(-5.3, 7.5); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-pythagoras-squares.png")

# Figure 3: rearrangement proof
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
a, b = 1.0, 2.0
s = a + b
ax = axes[0]
ax.add_patch(Rectangle((0, 0), s, s, fill=False, ec=BLACK, lw=2))
tris = [[(0, 0), (b, 0), (0, a)], [(b, 0), (s, 0), (s, b)], [(s, b), (s, s), (a, s)], [(a, s), (0, s), (0, a)]]
for t in tris:
    ax.add_patch(Polygon(t, closed=True, fc=ORANGE, ec=BLACK))
ax.add_patch(Polygon([(b, 0), (s, b), (a, s), (0, a)], closed=True, fc=L_RED, ec=RED, lw=2))
ax.text(s / 2, s / 2, "c x c", ha="center", va="center", fontsize=16, weight="bold")
ax.set_title("four triangles, plus a square c x c", fontsize=13)
ax = axes[1]
ax.add_patch(Rectangle((0, 0), s, s, fill=False, ec=BLACK, lw=2))
ax.add_patch(Rectangle((0, 0), b, b, fc=L_BLUE, ec=BLUE, lw=2)); ax.text(b / 2, b / 2, "b x b", ha="center", va="center", fontsize=16, weight="bold")
ax.add_patch(Rectangle((b, b), a, a, fc=L_GREEN, ec=GREEN, lw=2)); ax.text(b + a / 2, b + a / 2, "a x a", ha="center", va="center", fontsize=12, weight="bold")
for t in [[(b, 0), (s, 0), (s, b)], [(b, 0), (b, b), (s, b)], [(0, b), (b, b), (b, s)], [(0, b), (0, s), (b, s)]]:
    ax.add_patch(Polygon(t, closed=True, fc=ORANGE, ec=BLACK))
ax.set_title("the same four triangles, moved: a x a + b x b", fontsize=13)
for ax in axes:
    ax.set_xlim(-0.2, s + 0.2); ax.set_ylim(-0.2, s + 0.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-rearrangement.png")

# Figure 4: circle facts: unrolled wheel and pizza slices
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ax = axes[0]
ax.add_patch(Circle((0.5, 1.0), 0.5, fc=L_ORANGE, ec=BLACK, lw=2)); ax.plot([0.5, 1.0], [1.0, 1.0], color=GREEN, lw=3)
ax.text(0.75, 1.08, "r", fontsize=13, color=GREEN)
ax.plot([0.5, 0.5 + 2 * math.pi * 0.5], [0.45, 0.45], color=RED, lw=4)
ax.text(0.5 + math.pi * 0.5, 0.2, "one turn rolls 2 x pi x r = pi x diameter", ha="center", fontsize=12.5, color=RED)
ax.set_xlim(-0.1, 3.9); ax.set_ylim(0, 1.7); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("the edge of a circle", fontsize=13)
ax = axes[1]
n = 16; r = 1.0
for i in range(n):
    up = i % 2 == 0
    x0 = i * (math.pi * r / n)
    w = math.pi * r / n
    if up:
        pts = [(x0, 0), (x0 + 2 * w, 0), (x0 + w, r)]
    else:
        pts = [(x0 - w + w, r), (x0 + w + w, r), (x0 + w, 0)]
    ax.add_patch(Polygon(pts, closed=True, fc=L_BLUE if up else L_GREEN, ec=BLACK, lw=0.8))
ax.text(math.pi * r / 2 + 0.1, -0.25, "half the edge: pi x r", ha="center", fontsize=12.5)
ax.text(-0.25, 0.5, "r", fontsize=13)
ax.text(math.pi * r / 2 + 0.1, 1.15, "area = pi x r x r", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-0.4, 3.6); ax.set_ylim(-0.45, 1.4); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("slices laid top to tail make a near-rectangle", fontsize=13)
save(fig, "fig04-circle-facts.png")

# Figure 5: Monte Carlo pi
random.seed(3)
xs = [random.uniform(-1, 1) for _ in range(2000)]
ys = [random.uniform(-1, 1) for _ in range(2000)]
inside = [x * x + y * y <= 1 for x, y in zip(xs, ys)]
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.scatter([x for x, i in zip(xs, inside) if i], [y for y, i in zip(ys, inside) if i], s=6, color=BLUE, label="inside the circle")
ax.scatter([x for x, i in zip(xs, inside) if not i], [y for y, i in zip(ys, inside) if not i], s=6, color=RED, marker="x", label="outside")
ax.add_patch(Circle((0, 0), 1, fill=False, ec=BLACK, lw=2))
ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05); ax.set_aspect("equal")
ax.set_title(f"2000 points, {sum(inside)} inside: pi is about 4 x {sum(inside)}/2000 = {4 * sum(inside) / 2000:.3f}", fontsize=11.5)
ax.legend(loc="upper right", fontsize=10.5, framealpha=0.95)
save(fig, "fig05-monte-carlo-pi.png")

# Figure 6: arm reach ring
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.add_patch(Wedge((0, 0), 0.65, 0, 360, width=0.5, fc=L_GREEN, ec=GREEN, lw=2))
ax.plot([0], [0], "s", color=BLACK, ms=10); ax.text(0.02, -0.06, "shoulder", fontsize=11.5)
for (x, y) in [(0.30, 0.40), (0.60, 0.20), (0.10, 0.05), (0.0, 0.65), (0.5, 0.5)]:
    ok = 0.15 <= math.hypot(x, y) <= 0.65
    ax.plot([x], [y], "o" if ok else "X", color=BLUE if ok else RED, ms=12, mec=BLACK)
    ax.text(x + 0.03, y + 0.03, f"({x}, {y})", fontsize=11)
ax.plot([0, 0.367, 0.30], [0, 0.159, 0.40], color=ORANGE, lw=5, solid_capstyle="round")
ax.text(-0.62, -0.72, "green ring: every point the tip can reach (0.15 m to 0.65 m)", fontsize=11.5)
ax.set_xlim(-0.75, 0.85); ax.set_ylim(-0.78, 0.8); ax.set_aspect("equal"); ax.grid(alpha=0.3)
save(fig, "fig06-arm-reach.png")

# Figure 7: mower round a flower bed
fig, ax = plt.subplots(figsize=(7, 7))
ax.add_patch(Circle((0, 0), 1.5, fc=L_GREEN, ec=GREEN, lw=2)); ax.text(0, 0, "flower bed\nr = 1.5 m", ha="center", va="center", fontsize=12.5)
for r, col, st, lab in [(1.6, BLUE, "--", "inner wheel: 10.05 m"), (1.8, ORANGE, "-", "robot centre: 11.31 m"), (2.0, RED, ":", "outer wheel: 12.57 m")]:
    ax.add_patch(Circle((0, 0), r, fill=False, ec=col, lw=2.5, ls=st, label=lab))
ax.add_patch(Rectangle((1.6, -0.15), 0.4, 0.3, fc=ORANGE, ec=BLACK, zorder=5))
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4); ax.set_aspect("equal"); ax.axis("off"); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig07-flower-bed.png")
print("figures saved in", os.path.abspath(OUT))
