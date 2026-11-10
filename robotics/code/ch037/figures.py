# Figures for Chapter 37 - Numbers.
# Run:  python figures.py      (saves PNG files in ../../images/ch037/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch037")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=3))


# ---------- Figure 1: number line ----------
fig, ax = plt.subplots(figsize=(12, 3.8))
arrow(ax, (-7.6, 0), (7.6, 0), BLACK, 1.6, "<|-|>")
for n in range(-7, 8):
    ax.plot([n, n], [-0.12, 0.12], color=BLACK, lw=1.5)
    ax.text(n, -0.42, str(n), ha="center", fontsize=12)
arrow(ax, (0, 0.55), (5, 0.55), BLUE, 3)
ax.text(2.5, 0.75, "start at 0, go forward 5", ha="center", color=BLUE, fontsize=12.5)
arrow(ax, (5, 1.35), (-3, 1.35), RED, 3)
ax.text(1, 1.55, "then go backward 8:  5 + (-8) = -3", ha="center", color=RED, fontsize=12.5)
ax.plot([-3, -3], [0.08, 1.3], color=GREY, ls=":", lw=1.5)
ax.plot([5, 5], [0.08, 1.3], color=GREY, ls=":", lw=1.5)
ax.plot([-3], [0], "o", ms=15, color=ORANGE, mec=BLACK, zorder=4)
ax.text(-5.3, -0.95, "behind the start (negative)", ha="center", fontsize=12)
ax.text(5.3, -0.95, "in front of the start (positive)", ha="center", fontsize=12)
ax.set_xlim(-8, 8); ax.set_ylim(-1.2, 2); ax.axis("off")
save(fig, "fig01-number-line.png")

# ---------- Figure 2: equal fractions ----------
fig, axes = plt.subplots(3, 1, figsize=(11, 4.6))
for ax, (top, bottom, label) in zip(axes, [(1, 5, "1/5"), (2, 10, "2/10"), (12, 60, "12/60")]):
    w = 1 / bottom
    for i in range(bottom):
        ax.add_patch(Rectangle((i * w, 0), w, 1, fc=(L_BLUE if i < top else "white"), ec=BLACK, lw=(1.0 if bottom < 60 else 0.3)))
    ax.text(-0.02, 0.5, label, ha="right", va="center", fontsize=15, weight="bold")
    ax.set_xlim(-0.12, 1.01); ax.set_ylim(-0.05, 1.05); ax.axis("off")
save(fig, "fig02-equal-fractions.png")

# ---------- Figure 3: gear train ----------
fig, ax = plt.subplots(figsize=(13, 5.0))
stages = [(12, 60, 1.0), (15, 45, 5.6), (10, 40, 10.2)]
for i, (a, b, x) in enumerate(stages):
    ra, rb = a / 34, b / 34
    ax.add_patch(Circle((x, 2.2), ra, fc=L_ORANGE, ec=BLACK, lw=1.5))
    ax.add_patch(Circle((x + ra + rb, 2.2), rb, fc=L_GREEN, ec=BLACK, lw=1.5))
    ax.text(x, 2.2, str(a), ha="center", va="center", fontsize=12, weight="bold")
    ax.text(x + ra + rb, 2.2, str(b), ha="center", va="center", fontsize=12, weight="bold")
    ax.text(x + (ra + rb) / 2, 0.15, f"stage {i + 1}: {a} / {b} = 1/{b // a if b % a == 0 else b / a:g}", ha="center", fontsize=12.5)
ax.text(1.0, 4.35, "motor\n6000 rpm\n0.05 N m", ha="center", va="center", fontsize=12, color=BLUE)
ax.text(12.8, 4.35, "output\n100 rpm\n2.57 N m", ha="center", va="center", fontsize=12, color=BLUE)
for x1, x2 in [(3.1, 5.3), (7.75, 9.9)]:
    ax.plot([x1, x2], [2.2, 2.2], color=GREY, ls="--", lw=2, zorder=0)
ax.text(7.0, 4.75, "dashed line = two gears fixed on the same shaft", ha="center", fontsize=12, color="#555555")
ax.set_xlim(0, 14); ax.set_ylim(0, 5.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-gear-train.png")

# ---------- Figure 4: position and distance rolled ----------
moves = [1300, -650, 2600, -3900, 650]
pos, trav = [0], [0]
for m in moves:
    pos.append(pos[-1] + m)
    trav.append(trav[-1] + abs(m))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.axhline(0, color=BLACK, lw=1)
ax.plot(range(6), pos, "o-", color=BLUE, lw=2.5, ms=8, label="position (net)")
ax.plot(range(6), trav, "s--", color=GREEN, lw=2.5, ms=8, label="total rolled")
for i, v in enumerate(pos):
    ax.annotate(str(v), (i, v), textcoords="offset points", xytext=(0, -22 if i in (4, 5) else 10), ha="center", color=BLUE, fontsize=11.5)
ax.annotate(str(trav[-1]), (5, trav[-1]), textcoords="offset points", xytext=(-8, 8), ha="right", color=GREEN, fontsize=11.5)
ax.set_xlabel("move number"); ax.set_ylabel("encoder ticks"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
ax.set_ylim(-2000, 10300)
save(fig, "fig04-position-vs-travelled.png")

# ---------- Figure 5: percentage to PWM ----------
fig, ax = plt.subplots(figsize=(10, 4.8))
xs = list(range(-140, 141, 2))
ys = [min(abs(x), 100) / 100 * 255 * (1 if x >= 0 else -1) for x in xs]
ax.plot(xs, ys, color=GREEN, lw=3)
ax.axhline(0, color=BLACK, lw=1); ax.axvline(0, color=BLACK, lw=1)
ax.axvspan(100, 140, color=L_GREY); ax.axvspan(-140, -100, color=L_GREY)
ax.text(120, -130, "limited\nto 255", ha="center", fontsize=12); ax.text(-120, 130, "limited\nto -255", ha="center", fontsize=12)
ax.plot([50], [127.5], "o", color=BLUE, ms=9); ax.annotate("50% gives 128", (50, 127.5), xytext=(58, 70), fontsize=12, color=BLUE)
ax.plot([-25], [-63.75], "o", color=BLUE, ms=9); ax.annotate("-25% gives 64, backward", (-25, -63.75), xytext=(4, -105), fontsize=12, color=BLUE)
ax.set_xlabel("speed command (%)"); ax.set_ylabel("signed PWM value (sign = direction)")
ax.set_xlim(-140, 140); ax.set_ylim(-290, 290); ax.grid(alpha=0.3)
save(fig, "fig05-percent-to-pwm.png")
print("figures saved in", os.path.abspath(OUT))
