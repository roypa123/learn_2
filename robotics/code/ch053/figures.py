# Figures for Chapter 53 - Sequences, sums and sigma notation.
# Run:  python figures.py      (saves PNG files in ../../images/ch053/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch053")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


# Figure 1: arithmetic and geometric sequences
k = list(range(10))
fig, axes = plt.subplots(1, 2, figsize=(12.5, 4.6))
axes[0].bar(k, [2 + 3 * i for i in k], color=L_BLUE, edgecolor=BLUE)
axes[0].set_title("arithmetic: 2, 5, 8, ... (add 3 each time)", fontsize=12.5)
axes[1].bar(k, [0.5 ** i for i in k], color=L_GREEN, edgecolor=GREEN)
axes[1].set_title("geometric: 1, 0.5, 0.25, ... (multiply by 0.5)", fontsize=12.5)
for ax in axes:
    ax.set_xlabel("term number k (starting at 0)"); ax.set_xticks(k); ax.grid(alpha=0.3, axis="y")
save(fig, "fig01-two-sequences.png")

# Figure 2: Gauss pairing
fig, ax = plt.subplots(figsize=(11, 3.6))
n = 10
for i in range(1, n + 1):
    ax.add_patch(Rectangle((i - 1, 0), 0.9, i, fc=L_BLUE, ec=BLUE))
    ax.add_patch(Rectangle((i - 1, i), 0.9, n + 1 - i, fc=L_ORANGE, ec=ORANGE))
ax.text(n + 0.3, (n + 1) / 2, "each column is\n1 + 10 = 11 high", fontsize=12.5, va="center")
ax.text(4.5, -1.3, "blue: 1 + 2 + ... + 10.   orange: the same numbers backwards.   Together: 10 columns of 11.", ha="center", fontsize=12)
ax.set_xlim(-0.5, 14); ax.set_ylim(-2, 11.5); ax.axis("off")
save(fig, "fig02-gauss.png")

# Figure 3: halves filling a square
fig, ax = plt.subplots(figsize=(6.5, 6.5))
x0, y0, w, h = 0.0, 0.0, 1.0, 1.0
cols = [L_BLUE, L_GREEN, L_ORANGE, L_GREY]
labels = ["1/2", "1/4", "1/8", "1/16", "1/32", "1/64"]
for i in range(8):
    if i % 2 == 0:
        ax.add_patch(Rectangle((x0, y0), w / 2, h, fc=cols[i % 4], ec=BLACK))
        if i < len(labels):
            ax.text(x0 + w / 4, y0 + h / 2, labels[i], ha="center", va="center", fontsize=max(16 - 2 * i, 8))
        x0 += w / 2; w /= 2
    else:
        ax.add_patch(Rectangle((x0, y0), w, h / 2, fc=cols[i % 4], ec=BLACK))
        if i < len(labels):
            ax.text(x0 + w / 2, y0 + h / 4, labels[i], ha="center", va="center", fontsize=max(16 - 2 * i, 8))
        y0 += h / 2; h /= 2
ax.set_title("1/2 + 1/4 + 1/8 + ... fills the whole square: the sum is 1", fontsize=12)
ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-halves.png")

# Figure 4: anatomy of sigma
fig, ax = plt.subplots(figsize=(11, 4.4))
ax.text(1.0, 1.0, "Σ", fontsize=90, ha="center", va="center")
ax.text(1.0, 2.05, "n", fontsize=20, ha="center"); ax.text(1.0, -0.2, "i = 1", fontsize=20, ha="center")
ax.text(2.1, 1.0, "xᵢ", fontsize=34, va="center")
ax.annotate("stop at i = n", (1.15, 2.2), xytext=(3.4, 2.3), fontsize=13, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("start at i = 1", (1.35, -0.1), xytext=(3.4, -0.35), fontsize=13, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("add up this, for every i", (2.5, 1.0), xytext=(3.4, 1.0), fontsize=13, arrowprops=dict(arrowstyle="-|>"))
ax.text(7.6, 1.6, "total = 0", fontsize=14, family="DejaVu Sans Mono")
ax.text(7.6, 1.0, "for i in range(1, n + 1):", fontsize=14, family="DejaVu Sans Mono")
ax.text(7.6, 0.4, "    total += x[i]", fontsize=14, family="DejaVu Sans Mono")
ax.text(9.9, 2.3, "the same thing in Python", fontsize=12.5, ha="center", color=BLUE)
ax.set_xlim(0, 12.5); ax.set_ylim(-0.8, 2.8); ax.axis("off")
save(fig, "fig04-sigma.png")

# Figure 5: odometry steps
steps = [(0.10, 0), (0.10, 0), (0.10, 15), (0.10, 30), (0.10, 45), (0.10, 60), (0.10, 75), (0.10, 90), (0.10, 90), (0.10, 90)]
fig, ax = plt.subplots(figsize=(7.5, 7))
x = y = 0.0
for i, (d, hd) in enumerate(steps):
    nx, ny = x + d * math.cos(math.radians(hd)), y + d * math.sin(math.radians(hd))
    arrow(ax, (x, y), (nx, ny), BLUE, 2.5)
    x, y = nx, ny
ax.plot([0], [0], "s", color=ORANGE, mec=BLACK, ms=12, label="start")
ax.plot([x], [y], "o", color=RED, ms=11, label=f"end ({x:.3f}, {y:.3f})")
ax.plot([0, x], [0, y], color=GREY, ls="--", lw=1.5, label="straight line: 0.823 m")
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.grid(alpha=0.3); ax.set_aspect("equal"); ax.legend(loc="upper left")
ax.set_xlim(-0.1, 0.8); ax.set_ylim(-0.1, 0.8)
save(fig, "fig05-odometry.png")

# Figure 6: repeatability
visits = [(0.02, -0.01), (0.03, 0.02), (-0.01, 0.01), (0.04, 0.00), (0.01, -0.02), (0.02, 0.03), (0.00, 0.01), (0.03, -0.01), (0.05, 0.02), (0.01, 0.00)]
mx = sum(v[0] for v in visits) / 10; my = sum(v[1] for v in visits) / 10
fig, ax = plt.subplots(figsize=(7, 7))
ax.plot([v[0] for v in visits], [v[1] for v in visits], "o", color=BLUE, ms=10, label="ten visits")
ax.plot([0], [0], "+", color=BLACK, ms=22, mew=3, label="taught point")
ax.plot([mx], [my], "x", color=RED, ms=14, mew=3, label="centre of the visits")
ax.add_patch(Circle((mx, my), 0.043, fill=False, ec=GREEN, lw=2.5, ls="--"))
ax.text(mx + 0.002, my - 0.051, "repeatability circle, r = 0.043 mm", fontsize=11.5, color=GREEN, ha="center")
ax.set_xlabel("x error (mm)"); ax.set_ylabel("y error (mm)"); ax.grid(alpha=0.3); ax.set_aspect("equal"); ax.legend(loc="upper right", fontsize=11)
ax.set_xlim(-0.04, 0.08); ax.set_ylim(-0.05, 0.07)
save(fig, "fig06-repeatability.png")

# Figure 7: doses building up
fig, ax = plt.subplots(figsize=(10, 4.8))
amount = 0.0
ts, vs = [], []
for dose in range(8):
    for step in range(81):
        tt = dose * 8 + step * 0.1
        if step == 0:
            amount += 200
        ts.append(tt); vs.append(amount * 0.5 ** (step * 0.1 / 8))
    amount = amount * 0.5
ax.plot(ts, vs, color=BLUE, lw=2.5, label="amount in the body (mg)")
ax.axhline(400, color=BLACK, ls="--", lw=1.8, label="limit of the peaks: 200 / (1 - 0.5) = 400 mg")
ax.set_xlabel("time (hours)"); ax.set_ylabel("amount (mg)"); ax.grid(alpha=0.3); ax.legend(loc="lower right"); ax.set_ylim(0, 450)
save(fig, "fig07-doses.png")
print("figures saved in", os.path.abspath(OUT))
