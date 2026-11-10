# Figures for Chapter 20 — Repeating part 2: for loops and range.
# Run:  python figures.py      (saves PNG files in ../../images/ch020/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch020")
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


# ---------- Figure 1: for walks along a series ----------
fig, ax = plt.subplots(figsize=(13, 4.4))
ax.text(5.5, 4.1, "for letter in \"FRFL\":", ha="center", fontsize=17, family=MONO, weight="bold")
for i, ch in enumerate("FRFL"):
    ax.add_patch(Rectangle((1.7 + i * 2.0, 1.4), 1.6, 1.3, fc=L_BLUE, ec=BLACK, lw=1.5))
    ax.text(2.5 + i * 2.0, 2.05, ch, ha="center", va="center", fontsize=22, family=MONO, weight="bold")
    ax.text(2.5 + i * 2.0, 3.05, f"pass {i + 1}", ha="center", fontsize=12, color=BLUE, weight="bold")
    ax.text(2.5 + i * 2.0, 1.05, f"letter = '{ch}'", ha="center", fontsize=12, family=MONO)
for i in range(3):
    arrow(ax, (3.35 + i * 2.0, 2.05), (3.65 + i * 2.0, 2.05), ORANGE, 2.5)
ax.text(5.5, 0.35, "Python takes the items one at a time. No counter and no update line are needed.", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0.5, 10.5); ax.set_ylim(0.1, 4.5); ax.axis("off")
save(fig, "fig01-for-walks-along.png")

# ---------- Figure 2: what range makes ----------
fig, ax = plt.subplots(figsize=(13, 6.0))
rows = [("range(5)", 0, 5, 1), ("range(2, 6)", 2, 6, 1), ("range(0, 10, 2)", 0, 10, 2), ("range(10, 0, -3)", 10, 0, -3)]
for r, (code, a, b, st) in enumerate(rows):
    y = 3 - r * 1.1
    ax.text(-0.5, y, code, ha="right", va="center", fontsize=14, family=MONO, weight="bold")
    ax.plot([0, 10.5], [y, y], color=L_GREY, lw=2, zorder=0)
    for v in range(0, 11):
        ax.plot([v, v], [y - 0.07, y + 0.07], color=GREY, lw=1, zorder=0)
    v = a
    while (st > 0 and v < b) or (st < 0 and v > b):
        ax.plot(v, y, "o", color=BLUE, ms=22, zorder=2)
        ax.text(v, y, str(v), ha="center", va="center", color="white", fontsize=12, weight="bold", zorder=3)
        v += st
    ax.plot(b, y, "X", color=RED, ms=14, zorder=2)
    ax.text(b, y + 0.38, "stop", ha="center", color=RED, fontsize=11, weight="bold")
ax.text(4, 3.9, "range(start, stop, step): blue numbers are produced; the stop value (red X) never is", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-5.0, 10.8); ax.set_ylim(-0.7, 4.2); ax.axis("off")
save(fig, "fig02-what-range-makes.png")

# ---------- Figure 3: the route ----------
route = "FFRFFLFRFF"
x, y, h = 0, 0, 0
pts = [(0, 0)]
turns = []
for L in route:
    if L == "L":
        h = (h - 1) % 4; turns.append((x, y, "L"))
    elif L == "R":
        h = (h + 1) % 4; turns.append((x, y, "R"))
    else:
        dx, dy = [(0, 1), (1, 0), (0, -1), (-1, 0)][h]
        x += dx; y += dy
        pts.append((x, y))
fig, ax = plt.subplots(figsize=(10, 7.2))
for g in range(0, 6):
    ax.plot([g, g], [-0.5, 3.8], color=L_GREY, lw=1, zorder=0)
for g in range(0, 4):
    ax.plot([-0.5, 5.3], [g, g], color=L_GREY, lw=1, zorder=0)
for (a, b), (c, d) in zip(pts, pts[1:]):
    ax.add_patch(FancyArrowPatch((a, b), (c, d), arrowstyle="-|>", mutation_scale=18, color=BLUE, lw=3, zorder=2))
for (a, b, t) in turns:
    ax.text(a + 0.13, b + 0.15, t, fontsize=14, color=RED, weight="bold", zorder=4)
ax.plot(0, 0, "s", color=ORANGE, ms=18, mec=BLACK, zorder=3)
ax.text(-0.2, -0.32, "start", ha="center", fontsize=12)
ax.plot(4, 3, "*", color=ORANGE, ms=26, mec=BLACK, zorder=3)
ax.text(4.25, 3.15, "end (4, 3)", fontsize=12.5, weight="bold")
ax.plot([0, 4], [0, 3], color=GREY, ls=":", lw=2, zorder=1)
ax.text(2.3, 1.05, "5.0 m in a\nstraight line", fontsize=12, color=GREY, ha="left", va="top")
ax.text(2.4, 4.15, 'route = "FFRFFLFRFF"   7 m driven', ha="center", fontsize=14, family=MONO, weight="bold")
ax.set_xlim(-0.7, 5.5); ax.set_ylim(-0.7, 4.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-the-route.png")

# ---------- Figure 4: nested loops as a serpentine map ----------
W, H = 6, 4
fig, ax = plt.subplots(figsize=(11.5, 6.6))
order = {}
for row in range(H):
    for col in range(W):
        o = row * W + (col if row % 2 == 0 else W - 1 - col)
        order[o] = (col, row)
        ax.add_patch(Rectangle((col, H - 1 - row), 1, 1, fc=L_BLUE if row % 2 == 0 else L_GREEN, ec=BLACK))
        ax.text(col + 0.2, H - 1 - row + 0.78, str(o), ha="center", va="center", fontsize=12.5, weight="bold", family=MONO)
for o in range(W * H - 1):
    a, b = order[o], order[o + 1]
    ax.add_patch(FancyArrowPatch((a[0] + 0.5, H - 1 - a[1] + 0.42), (b[0] + 0.5, H - 1 - b[1] + 0.42), arrowstyle="-|>", mutation_scale=13, color=ORANGE, lw=2.2))
for row in range(H):
    ax.text(-0.3, H - 1 - row + 0.5, f"row {row}", ha="right", va="center", fontsize=12.5, color=RED, weight="bold")
for col in range(W):
    ax.text(col + 0.5, 4.2, f"col {col}", ha="center", fontsize=12.5, color=BLUE, weight="bold")
ax.text(3, 4.75, "outer loop: rows (red). Inner loop: columns (blue), all of them for EACH row", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-1.2, 6.2); ax.set_ylim(-0.2, 5.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-nested-loops-map.png")

# ---------- Figure 5: the gain sweep ----------
gains = [k * 0.5 for k in range(1, 9)]
steps = [16, 9, 7, 6, 7, 8, 12, 60]
low = [0.308, 0.306, 0.305, 0.300, 0.281, 0.262, 0.250, 0.250]
fig, ax = plt.subplots(figsize=(13, 5.0))
cols = [GREEN if l >= 0.29 else RED for l in low]
ax.bar(gains, steps, width=0.35, color=cols, ec=BLACK)
for g, s in zip(gains, steps):
    ax.text(g, s + 1.2, str(s), ha="center", fontsize=12, weight="bold")
ax.set_xlabel("gain"); ax.set_ylabel("steps to settle (60 = never)")
ax.set_ylim(0, 68); ax.set_xticks(gains); ax.grid(axis="y", alpha=0.3)
ax.bar([0], [0], color=GREEN, label="no overshoot"); ax.bar([0], [0], color=RED, label="goes past the setpoint")
ax.legend(loc="upper center", framealpha=1)
ax.annotate("best without overshoot", xy=(2.0, 11), xytext=(1.3, 30), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlim(0.2, 4.4)
save(fig, "fig05-gain-sweep.png")
print("figures saved in", os.path.abspath(OUT))
