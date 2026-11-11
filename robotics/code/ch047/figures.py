# Figures for Chapter 47 - Angles: degrees and radians.
# Run:  python figures.py      (saves PNG files in ../../images/ch047/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, FancyArrowPatch, Arc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch047")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.5):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


# Figure 1: degrees and radians round a circle
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.add_patch(Circle((0, 0), 1, fill=False, ec=BLACK, lw=2))
marks = [(0, "0", "0"), (30, "30", "pi/6"), (45, "45", "pi/4"), (90, "90", "pi/2"), (180, "180", "pi"), (270, "270", "3pi/2"), (135, "135", "3pi/4")]
for d, ds, rs in marks:
    t = math.radians(d)
    ax.plot([0, math.cos(t)], [0, math.sin(t)], color=GREY, lw=1.2)
    ax.text(1.18 * math.cos(t), 1.18 * math.sin(t), f"{ds} deg", ha="center", va="center", fontsize=12, color=BLUE)
    ax.text(0.78 * math.cos(t), 0.78 * math.sin(t) + 0.05, rs, ha="center", va="center", fontsize=12, color=GREEN, bbox=dict(fc="white", ec="none", pad=0.5))
ax.add_patch(Arc((0, 0), 0.4, 0.4, theta1=0, theta2=340, color=RED, lw=2))
ax.text(0.05, -0.33, "anticlockwise is positive", fontsize=11.5, color=RED)
ax.text(-1.45, -1.35, "blue: degrees    green: radians", fontsize=12)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-circle.png")

# Figure 2: one radian
fig, ax = plt.subplots(figsize=(7.5, 6.5))
ax.add_patch(Circle((0, 0), 2, fill=False, ec=GREY, lw=1.5, ls="--"))
ax.add_patch(Wedge((0, 0), 2, 0, math.degrees(1), fc=L_BLUE, ec=BLUE, lw=2))
ax.plot([0, 2], [0, 0], color=GREEN, lw=4); ax.text(1.0, -0.25, "radius r", ha="center", fontsize=13, color=GREEN)
th = np.linspace(0, 1, 50)
ax.plot(2 * np.cos(th), 2 * np.sin(th), color=RED, lw=5)
ax.text(2.15, 0.95, "arc as long\nas the radius", fontsize=13, color=RED)
ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=0, theta2=math.degrees(1), color=BLACK, lw=2))
ax.text(0.55, 0.2, "1 radian\n(57.3 deg)", fontsize=12)
ax.set_xlim(-2.3, 3.4); ax.set_ylim(-2.3, 2.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-one-radian.png")

# Figure 3: maths angle against compass bearing
fig, axes = plt.subplots(1, 2, figsize=(12, 5.6))
for ax, title in zip(axes, ["maths angle: from east (x axis), anticlockwise", "compass bearing: from north, clockwise"]):
    ax.add_patch(Circle((0, 0), 1, fill=False, ec=GREY, lw=1.5))
    for lab, (x, y) in [("E", (1.15, 0)), ("N", (0, 1.15)), ("W", (-1.15, 0)), ("S", (0, -1.15))]:
        ax.text(x, y, lab, ha="center", va="center", fontsize=14, weight="bold")
    ax.set_title(title, fontsize=12.5); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_aspect("equal"); ax.axis("off")
t = math.radians(30)
for ax in axes:
    arrow(ax, (0, 0), (math.cos(t), math.sin(t)), ORANGE, 3.5)
axes[0].add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=30, color=BLUE, lw=2.5)); axes[0].text(0.38, 0.06, "30", fontsize=13, color=BLUE)
axes[1].add_patch(Arc((0, 0), 0.6, 0.6, theta1=30, theta2=90, color=GREEN, lw=2.5)); axes[1].text(0.12, 0.42, "60", fontsize=13, color=GREEN)
save(fig, "fig03-maths-vs-compass.png")

# Figure 4: wrapping sawtooth
a = np.linspace(-540, 540, 2161)
w = (a + 180) % 360 - 180
w[np.abs(np.diff(w, prepend=w[0])) > 100] = np.nan
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.plot(a, a, color=BLACK, ls="--", lw=1.5, label="angle before wrapping")
ax.plot(a, w, color=BLUE, lw=3, label="wrap_180(angle)")
for x0 in (725 - 720, 190, -190):
    pass
ax.plot([190], [-170], "o", color=RED, ms=9); ax.annotate("190 becomes -170", (190, -170), xytext=(240, -330), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.axhspan(-180, 180, color=L_GREY, alpha=0.5)
ax.set_xlabel("angle (degrees)"); ax.set_ylabel("wrapped angle (degrees)"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
ax.set_xlim(-540, 540); ax.set_ylim(-560, 560); ax.set_xticks(range(-540, 541, 180)); ax.set_yticks(range(-540, 541, 180))
save(fig, "fig04-wrap.png")

# Figure 5: shortest turn
fig, ax = plt.subplots(figsize=(7, 7))
ax.add_patch(Circle((0, 0), 1, fill=False, ec=GREY, lw=1.5))
for deg, lab, ha in [(350, "heading 350", "right"), (10, "target 10", "left")]:
    t = math.radians(90 - deg)
    arrow(ax, (0, 0), (math.cos(t), math.sin(t)), ORANGE if deg == 350 else GREEN, 3.5)
    ax.text(1.12 * math.cos(t), 1.12 * math.sin(t), lab, ha=ha, fontsize=13)
ax.add_patch(Arc((0, 0), 1.5, 1.5, theta1=80, theta2=100, color=BLUE, lw=4))
ax.text(0, -0.3, "+20: the short way (blue)", ha="center", fontsize=12.5, color=BLUE)
ax.add_patch(Arc((0, 0), 2.6, 2.6, theta1=100, theta2=440, color=RED, lw=2, ls="--"))
ax.text(0, -1.5, "-340: the long way round", ha="center", fontsize=12.5, color=RED)
ax.text(0, 1.45, "N", ha="center", fontsize=14, weight="bold")
ax.set_xlim(-1.7, 1.7); ax.set_ylim(-1.75, 1.75); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-shortest-turn.png")

# Figure 6: heading hold with and without wrapping (total angle turned)
def run(wrap):
    h = 350.0; turned = 0.0; out = [0.0]
    for _ in range(26):
        e = 20.0 - h
        if wrap:
            e = (e + 180) % 360 - 180
        step = max(-15, min(15, 0.5 * e))
        h = (h + step) % 360; turned += step; out.append(turned)
    return out
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(range(27), run(False), "s--", color=RED, lw=2, ms=6, label="error not wrapped")
ax.plot(range(27), run(True), "o-", color=BLUE, lw=2.5, ms=6, label="error wrapped")
ax.axhline(30, color=BLACK, ls="--", lw=1.5); ax.axhline(-330, color=BLACK, ls="--", lw=1.5)
ax.text(14, 45, "+30: heading 20 reached the short way", fontsize=12)
ax.text(0.5, -312, "-330: heading 20 reached the long way", fontsize=12)
ax.set_xlabel("step"); ax.set_ylabel("total angle turned (degrees)"); ax.grid(alpha=0.3); ax.legend(loc="center left", fontsize=11)
ax.set_ylim(-360, 80)
save(fig, "fig06-heading-hold.png")
print("figures saved in", os.path.abspath(OUT))
