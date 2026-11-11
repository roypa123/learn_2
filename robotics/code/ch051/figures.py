# Figures for Chapter 51 - Trigonometry part 3: the law of sines and the law of cosines.
# Run:  python figures.py      (saves PNG files in ../../images/ch051/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, Rectangle, FancyArrowPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch051")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


def ang(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


# Figure 1: naming a triangle
A, B, C = (0, 0), (6, 0), (2.2, 3.4)
fig, ax = plt.subplots(figsize=(9, 5.4))
ax.add_patch(Polygon([A, B, C], closed=True, fc=L_BLUE, ec=BLACK, lw=2))
for P, lab, off in [(A, "A", (-0.35, -0.3)), (B, "B", (0.15, -0.3)), (C, "C", (-0.1, 0.2))]:
    ax.text(P[0] + off[0], P[1] + off[1], lab, fontsize=16, weight="bold", color=RED)
ax.text(3.0, -0.45, "c (opposite C)", ha="center", fontsize=13, color=BLUE)
ax.text(4.4, 1.9, "a (opposite A)", fontsize=13, color=BLUE)
ax.text(0.3, 1.9, "b (opposite B)", fontsize=13, color=BLUE, ha="right")
ax.add_patch(Arc(A, 1.2, 1.2, theta1=0, theta2=ang(A, C), color=RED, lw=2.5))
ax.add_patch(Arc(B, 1.2, 1.2, theta1=ang(B, C), theta2=180, color=RED, lw=2.5))
ax.add_patch(Arc(C, 1.2, 1.2, theta1=ang(C, A), theta2=ang(C, B) + 360, color=RED, lw=2.5))
ax.set_xlim(-1.5, 7); ax.set_ylim(-0.8, 4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-names.png")

# Figure 2: law of cosines from a dropped height
fig, ax = plt.subplots(figsize=(9, 5.4))
ax.add_patch(Polygon([A, B, C], closed=True, fc=L_BLUE, ec=BLACK, lw=2))
ax.plot([C[0], C[0]], [0, C[1]], color=GREEN, lw=3, ls="--"); ax.text(C[0] + 0.1, 1.5, "h", fontsize=15, color=GREEN)
ax.add_patch(Rectangle((C[0], 0), 0.25, 0.25, fill=False, ec=BLACK))
ax.plot([0, C[0]], [-0.25, -0.25], color=ORANGE, lw=4); ax.text(C[0] / 2, -0.6, "b cos A", ha="center", fontsize=13, color=ORANGE)
ax.plot([C[0], 6], [-0.25, -0.25], color=RED, lw=4); ax.text((C[0] + 6) / 2, -0.6, "c - b cos A", ha="center", fontsize=13, color=RED)
ax.text(0.6, 1.9, "b", fontsize=15); ax.text(4.3, 1.9, "a", fontsize=15); ax.text(-0.35, -0.1, "A", fontsize=15, color=RED)
ax.text(3.0, 3.6, "h = b sin A,   then Pythagoras in the right-hand triangle", ha="center", fontsize=12.5)
ax.set_xlim(-1, 7); ax.set_ylim(-1.0, 4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-cosine-proof.png")

# Figure 3: ambiguous case
fig, ax = plt.subplots(figsize=(10, 5))
Ap = (0, 0)
Aang = math.radians(35)
b = 5.0
Cp = (b * math.cos(Aang), b * math.sin(Aang))
a = 3.3
dx = math.sqrt(a * a - Cp[1] ** 2)
B1, B2 = (Cp[0] - dx, 0), (Cp[0] + dx, 0)
ax.plot([-0.3, 8], [0, 0], color=GREY, lw=1.5)
ax.add_patch(Polygon([Ap, B2, Cp], closed=True, fc=L_GREEN, ec=GREEN, lw=2, alpha=0.7))
ax.add_patch(Polygon([Ap, B1, Cp], closed=True, fc=L_ORANGE, ec=ORANGE, lw=2, alpha=0.8))
ax.add_patch(Arc(Cp, 2 * a, 2 * a, theta1=200, theta2=340, color=BLUE, lw=1.8, ls=":"))
ax.text(Ap[0] - 0.3, -0.35, "A", fontsize=15, color=RED); ax.text(Cp[0], Cp[1] + 0.2, "C", fontsize=15, color=RED, ha="center")
ax.text(B1[0], -0.45, "B (one answer)", fontsize=12, ha="center", color=ORANGE); ax.text(B2[0], -0.45, "B (the other)", fontsize=12, ha="center", color=GREEN)
ax.text(1.4, 1.65, "b = 5", fontsize=13, rotation=35)
ax.text(5.9, 2.0, "a = 3.3 can swing\nto two places", fontsize=12, color=BLUE)
ax.set_xlim(-0.8, 8.2); ax.set_ylim(-0.9, 3.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-ambiguous.png")

# Figure 4: two-link arm, both answers
L1, L2 = 0.40, 0.25
tx, ty = 0.30, 0.40
fig, ax = plt.subplots(figsize=(8, 7))
for sh, el, col, st, lab in [(82.82, -82.10, BLUE, "-", "elbow up"), (23.44, 82.10, ORANGE, "--", "elbow down")]:
    s = math.radians(sh); e = math.radians(el)
    ex, ey = L1 * math.cos(s), L1 * math.sin(s)
    ax.plot([0, ex, tx], [0, ey, ty], color=col, lw=5, ls=st, solid_capstyle="round", label=f"{lab}: shoulder {sh:.1f}, elbow {el:.1f}")
    ax.plot([ex], [ey], "o", color=col, ms=12, mec=BLACK)
ax.plot([0, tx], [0, ty], color=GREY, lw=1.5, ls=":"); ax.text(0.17, 0.17, "d = 0.5", fontsize=12, rotation=53, color="#555555")
ax.plot([0], [0], "s", color=BLACK, ms=12); ax.plot([tx], [ty], "*", color=RED, ms=22, zorder=6)
ax.text(tx + 0.02, ty + 0.03, "target (0.3, 0.4)", fontsize=12)
ax.set_xlim(-0.2, 0.6); ax.set_ylim(-0.1, 0.6); ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.legend(loc="lower right", fontsize=11)
save(fig, "fig04-arm-two-answers.png")

# Figure 5: stereo triangulation
fig, ax = plt.subplots(figsize=(7.5, 7))
Lc, Rc = (0, 0), (0.2, 0)
obj = (0.134, 0.758)
ax.add_patch(Polygon([Lc, Rc, obj], closed=True, fc=L_GREY, ec=BLACK, lw=1.5))
for P, lab, ha in [(Lc, "left camera", "right"), (Rc, "right camera", "left")]:
    ax.add_patch(Rectangle((P[0] - 0.03, P[1] - 0.04), 0.06, 0.04, fc=ORANGE, ec=BLACK))
    ax.text(P[0], -0.1, lab, ha=ha, fontsize=11.5)
ax.plot([obj[0]], [obj[1]], "o", color=BLUE, ms=14); ax.text(obj[0] + 0.03, obj[1], "object", fontsize=12.5)
ax.add_patch(Arc(Lc, 0.2, 0.2, theta1=0, theta2=80, color=RED, lw=2.5)); ax.text(0.05, 0.03, "80", fontsize=12, color=RED)
ax.add_patch(Arc(Rc, 0.2, 0.2, theta1=95, theta2=180, color=RED, lw=2.5)); ax.text(0.1, 0.06, "85", fontsize=12, color=RED)
ax.add_patch(Arc(obj, 0.3, 0.3, theta1=ang(obj, Lc), theta2=ang(obj, Rc) + 360, color=GREEN, lw=2.5)); ax.text(obj[0] - 0.02, obj[1] - 0.24, "15", fontsize=12, color=GREEN)
ax.text(0.1, -0.17, "baseline 0.20 m", ha="center", fontsize=12)
ax.text(-0.18, 0.4, "0.770 m", fontsize=12.5, rotation=80)
ax.set_xlim(-0.3, 0.5); ax.set_ylim(-0.22, 0.85); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-stereo.png")

# Figure 6: wind triangle
fig, ax = plt.subplots(figsize=(8, 6))
air = (15 * math.cos(math.radians(60)), 15 * math.sin(math.radians(60)))
wind = (5, 0)
ground = (air[0] + wind[0], air[1] + wind[1])
arrow(ax, (0, 0), air, BLUE, 3.5); ax.text(3.4, 7.4, "air speed 15 m/s\n(where the drone points)", fontsize=12, color=BLUE, ha="right")
arrow(ax, air, ground, GREEN, 3.5); ax.text(air[0] + 0.5, air[1] + 0.4, "wind 5 m/s", fontsize=12, color=GREEN)
arrow(ax, (0, 0), ground, RED, 3.5); ax.text(7.0, 5.0, "ground speed 18.0 m/s\n(how it really moves)", fontsize=12, color=RED)
ax.add_patch(Arc(air, 3, 3, theta1=240, theta2=360, color=BLACK, lw=1.8)); ax.text(air[0] + 0.3, air[1] - 2.0, "120", fontsize=12)
ax.set_xlim(-6, 14); ax.set_ylim(-0.8, 14.5); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-wind.png")
print("figures saved in", os.path.abspath(OUT))
