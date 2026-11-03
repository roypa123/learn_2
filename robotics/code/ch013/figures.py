# Figures for Chapter 13 — Numbers and arithmetic.
# Run:  python figures.py      (saves PNG files in ../../images/ch013/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Wedge

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch013")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
PURPLE = "#CC79A7"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11, family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family)


# ---------- Figure 1: counting (int) and measuring (float) ----------
fig, axes = plt.subplots(2, 1, figsize=(13, 5.6))
ax = axes[0]
ax.axhline(0, color=BLACK, lw=1.5)
for k in range(0, 9):
    ax.plot(k, 0, "o", color=BLUE, ms=12)
    ax.text(k, -0.45, str(k), ha="center", fontsize=12, family=MONO)
ax.text(-0.6, 0.55, "int: COUNTING - only whole steps (encoder ticks, wheels, loops, people)", fontsize=12.5, color=BLUE, weight="bold")
ax.set_xlim(-0.7, 8.7); ax.set_ylim(-0.8, 0.9); ax.axis("off")
ax = axes[1]
ax.plot([0, 8], [0, 0], color=ORANGE, lw=6, solid_capstyle="round")
for k in range(0, 9):
    ax.plot([k, k], [-0.12, 0.12], color=BLACK, lw=1.5)
    ax.text(k, -0.45, f"{k}.0", ha="center", fontsize=12, family=MONO)
for v, lab in [(0.065, "0.065"), (3.704, "3.704"), (6.28, "6.28")]:
    ax.plot(v, 0, "v", color=RED, ms=12)
    ax.text(v, 0.28, lab, ha="center", fontsize=11, color=RED, family=MONO)
ax.text(-0.6, 0.62, "float: MEASURING - any value in between (distance, speed, voltage, angle)", fontsize=12.5, color=ORANGE, weight="bold")
ax.set_xlim(-0.7, 8.7); ax.set_ylim(-0.8, 0.95); ax.axis("off")
save(fig, "fig01-int-and-float.png")

# ---------- Figure 2: // and % with encoder ticks ----------
fig, ax = plt.subplots(figsize=(13.5, 4.6))
for i in range(3):
    ax.add_patch(Rectangle((i * 540, 0), 540, 1, fc=L_BLUE, ec=BLACK, lw=1.5))
    ax.text(i * 540 + 270, 0.5, f"turn {i + 1}\n540 ticks", ha="center", va="center", fontsize=12)
ax.add_patch(Rectangle((1620, 0), 380, 1, fc=L_ORANGE, ec=BLACK, lw=1.5))
ax.add_patch(Rectangle((2000, 0), 160, 1, fc="white", ec=GREY, lw=1.2, ls="--"))
ax.text(1810, 0.5, "380\nleftover", ha="center", va="center", fontsize=12)
ax.text(2080, 0.5, "not\nyet", ha="center", va="center", fontsize=10, color=GREY)
ax.annotate("", xy=(0, 1.35), xytext=(2000, 1.35), arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.5))
ax.text(1000, 1.5, "2000 ticks counted", ha="center", fontsize=12.5, weight="bold")
ax.text(810, -0.45, "2000 // 540 = 3   (whole turns)", ha="center", fontsize=13, family=MONO, color=BLUE, weight="bold")
ax.text(1810, -0.45, "2000 % 540 = 380", ha="center", fontsize=13, family=MONO, color=ORANGE, weight="bold")
ax.text(1080, -0.95, "check: 3 x 540 + 380 = 2000        and        2000 / 540 = 3.7037...", ha="center", fontsize=12)
ax.set_xlim(-50, 2200); ax.set_ylim(-1.2, 1.8); ax.axis("off")
save(fig, "fig02-floor-division-and-remainder.png")

# ---------- Figure 3: order of operations ----------
fig, ax = plt.subplots(figsize=(13, 6.2))
levels = [("1", "( )", "brackets: always first", L_RED),
          ("2", "**", "power (from the RIGHT: 2 ** 3 ** 2 = 2 ** 9)", L_ORANGE),
          ("3", "*   /   //   %", "multiply and divide (from the left)", L_BLUE),
          ("4", "+   -", "add and subtract (from the left)", L_GREEN)]
for i, (n, ops, txt, c) in enumerate(levels):
    y = 4.2 - i * 1.15
    w = 3.0 + i * 1.2
    box(ax, 4.0 - w / 2, y, w, 0.9, ops, c, 15, MONO)
    ax.text(0.0 - 0.4, y + 0.45, n, fontsize=16, weight="bold", va="center")
    ax.text(7.6, y + 0.45, txt, fontsize=12, va="center")
ax.text(6.5, 5.55, "Which operation happens first?", ha="center", fontsize=14, weight="bold")
ax.text(6.5, -0.35, "2 + 3 * 4  ->  2 + 12  ->  14          (2 + 3) * 4  ->  5 * 4  ->  20", ha="center", fontsize=13, family=MONO)
ax.set_xlim(-0.8, 13.5); ax.set_ylim(-0.7, 5.9); ax.axis("off")
save(fig, "fig03-order-of-operations.png")

# ---------- Figure 4: compass wrap-around with % 360 ----------
fig, ax = plt.subplots(figsize=(9, 9))
ax.add_patch(Circle((0, 0), 1.0, fc="white", ec=BLACK, lw=2))
for d in range(0, 360, 30):
    a = math.radians(90 - d)
    ax.plot([0.92 * math.cos(a), math.cos(a)], [0.92 * math.sin(a), math.sin(a)], color=BLACK, lw=1.5)
    ax.text(1.12 * math.cos(a), 1.12 * math.sin(a), str(d), ha="center", va="center", fontsize=11)
for d, lab in [(0, "N"), (90, "E"), (180, "S"), (270, "W")]:
    a = math.radians(90 - d)
    ax.text(0.78 * math.cos(a), 0.78 * math.sin(a), lab, ha="center", va="center", fontsize=14, weight="bold", color=GREY)
ax.add_patch(Wedge((0, 0), 0.6, 90 - 20, 90 + 10, width=0.08, fc=BLUE, ec=BLUE))
for d, col, lab in [(350, GREY, "start 350"), (20, BLUE, "350 + 30 = 380\n380 % 360 = 20")]:
    a = math.radians(90 - d)
    ax.annotate("", xy=(0.95 * math.cos(a), 0.95 * math.sin(a)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=3))
ax.text(-0.75, 1.45, "start: 350", fontsize=12, color=GREY, weight="bold")
ax.text(0.35, 1.45, "turn right 30:\n(350 + 30) % 360 = 20", fontsize=12, color=BLUE, weight="bold")
ax.text(0, -1.45, "% 360 keeps any heading between 0 and 359:\n380 -> 20     -30 -> 330     1055 -> 335", ha="center",
        fontsize=12.5, family=MONO)
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.75, 1.75); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-heading-wraparound.png")

# ---------- Figure 5: rounding to the nearest EVEN at .5 ----------
fig, ax = plt.subplots(figsize=(13, 3.8))
ax.axhline(0, color=BLACK, lw=1.5)
for k in range(0, 5):
    ax.plot([k, k], [-0.1, 0.1], color=BLACK, lw=1.5)
    ax.text(k, -0.38, str(k), ha="center", fontsize=13, weight="bold", family=MONO)
for v, r in [(0.5, 0), (1.5, 2), (2.5, 2), (3.5, 4)]:
    ax.plot(v, 0, "o", color=RED, ms=10)
    ax.text(v, 0.32, f"round({v})", ha="center", fontsize=11, family=MONO, color=RED)
    ax.annotate("", xy=(r, 0.08), xytext=(v, 0.08), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2,
                connectionstyle="arc3,rad=-0.5" if r > v else "arc3,rad=0.5"))
for v in (1.4, 2.7):
    ax.plot(v, 0, "o", color=BLUE, ms=8)
ax.text(1.4, -0.65, "1.4 -> 1", ha="center", fontsize=11, color=BLUE, family=MONO)
ax.text(2.7, -0.65, "2.7 -> 3", ha="center", fontsize=11, color=BLUE, family=MONO)
ax.text(2.0, 0.85, "Exactly halfway (.5)? Python goes to the nearest EVEN number: 0, 2, 2, 4", ha="center", fontsize=12.5, weight="bold")
ax.set_xlim(-0.4, 4.4); ax.set_ylim(-0.85, 1.05); ax.axis("off")
save(fig, "fig05-round-half-to-even.png")
print("figures saved in", os.path.abspath(OUT))
