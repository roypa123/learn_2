# Figures for Chapter 21 — Lists.
# Run:  python figures.py      (saves PNG files in ../../images/ch021/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch021")
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


def cells(ax, x0, y, items, face=L_BLUE, w=1.3, h=0.8, size=13, hi=None):
    for i, v in enumerate(items):
        c = L_ORANGE if hi is not None and i == hi else face
        ax.add_patch(Rectangle((x0 + i * w, y), w, h, fc=c, ec=BLACK, lw=1.4))
        ax.text(x0 + i * w + w / 2, y + h / 2, str(v), ha="center", va="center", fontsize=size, family=MONO, weight="bold")


# ---------- Figure 1: a list ----------
fig, ax = plt.subplots(figsize=(13, 4.2))
r = [0.52, 0.51, 0.53, 0.5]
cells(ax, 3.0, 1.2, r, w=1.7, h=1.0, size=16)
for i in range(4):
    ax.text(3.85 + i * 1.7, 2.55, str(i), ha="center", fontsize=15, color=BLUE, weight="bold", family=MONO)
    ax.text(3.85 + i * 1.7, 0.85, str(i - 4), ha="center", fontsize=14, color=RED, weight="bold", family=MONO)
ax.text(2.7, 2.55, "index", ha="right", fontsize=12.5, color=BLUE)
ax.text(2.7, 0.85, "from the end", ha="right", fontsize=12.5, color=RED)
ax.text(6.4, 3.4, "readings = [0.52, 0.51, 0.53, 0.5]", ha="center", fontsize=16, family=MONO, weight="bold")
ax.text(6.4, 0.2, "one name, many values: readings[0] is 0.52 and readings[-1] is 0.5", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0.6, 11.4); ax.set_ylim(0, 3.8); ax.axis("off")
save(fig, "fig01-a-list.png")

# ---------- Figure 2: changing a list ----------
fig, ax = plt.subplots(figsize=(13.5, 7.0))
rows = [("m = [1, 2, 3]", [1, 2, 3], None, ""),
        ("m.append(4)", [1, 2, 3, 4], 3, "adds at the END"),
        ("m.insert(0, 9)", [9, 1, 2, 3, 4], 0, "adds at index 0; the others shift right"),
        ("m.pop()", [9, 1, 2, 3], None, "removes the LAST and gives it back: 4"),
        ("m.pop(0)", [1, 2, 3], None, "removes index 0 and gives it back: 9"),
        ("m.remove(2)", [1, 3], None, "removes the first item EQUAL to 2")]
for i, (code, items, hi, note) in enumerate(rows):
    y = 6.0 - i * 1.15
    ax.text(3.2, y + 0.4, code, ha="right", va="center", fontsize=13.5, family=MONO, weight="bold")
    cells(ax, 3.5, y, items, hi=hi, w=0.95, h=0.8)
    ax.text(8.5, y + 0.4, note, va="center", fontsize=12)
ax.set_xlim(0, 14); ax.set_ylim(-0.1, 7.0); ax.axis("off")
save(fig, "fig02-changing-a-list.png")

# ---------- Figure 3: two names, one list ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
ax = axes[0]
ax.text(3.0, 4.4, "b = a   (the same list)", ha="center", fontsize=14, weight="bold", color=RED)
cells(ax, 1.05, 1.0, [1, 2, 3], w=1.3)
for name, x in [("a", 1.9), ("b", 4.1)]:
    ax.add_patch(FancyBboxPatch((x - 0.3, 2.9), 0.6, 0.55, boxstyle="round,pad=0.02,rounding_size=0.1", fc=L_ORANGE, ec=BLACK))
    ax.text(x, 3.17, name, ha="center", va="center", fontsize=14, family=MONO, weight="bold")
    arrow(ax, (x, 2.88), (3.0 if x > 3 else 2.4, 1.85), ORANGE)
ax.text(3.0, 0.3, "b.append(3) also changes a", ha="center", fontsize=13, family=MONO)
ax.set_xlim(0, 6); ax.set_ylim(0, 4.8); ax.axis("off")
ax = axes[1]
ax.text(3.0, 4.4, "c = a.copy()   (two lists)", ha="center", fontsize=14, weight="bold", color=GREEN)
cells(ax, 0.1, 1.0, [1, 2, 3], w=0.9)
cells(ax, 3.3, 1.0, [1, 2, 3, 9], w=0.7, hi=3)
for name, x, tx in [("a", 1.45, 1.45), ("c", 4.7, 4.7)]:
    ax.add_patch(FancyBboxPatch((x - 0.3, 2.9), 0.6, 0.55, boxstyle="round,pad=0.02,rounding_size=0.1", fc=L_ORANGE, ec=BLACK))
    ax.text(x, 3.17, name, ha="center", va="center", fontsize=14, family=MONO, weight="bold")
    arrow(ax, (x, 2.88), (tx, 1.85), ORANGE)
ax.text(3.0, 0.3, "c.append(9) leaves a alone", ha="center", fontsize=13, family=MONO)
ax.set_xlim(0, 6.2); ax.set_ylim(0, 4.8); ax.axis("off")
save(fig, "fig03-two-names-one-list.png")

# ---------- Figure 4: mean and median with a spike ----------
good = [0.52, 0.51, 0.53, 3.91, 0.50, 0.52]
fig, ax = plt.subplots(figsize=(13, 5.0))
ax.plot(range(1, 7), good, "o-", color=BLUE, ms=9, lw=2, label="believable readings")
ax.axhline(sum(good) / len(good), color=RED, lw=2.5, label="mean 1.082 m (pulled up by the spike)")
ax.axhline(0.52, color=GREEN, lw=2.5, label="median 0.520 m")
ax.annotate("one spike: 3.91 m", xy=(4, 3.91), xytext=(4.5, 3.4), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("reading number"); ax.set_ylabel("distance (m)"); ax.grid(alpha=0.3)
ax.set_ylim(0, 4.4); ax.legend(loc="upper left", framealpha=1)
save(fig, "fig04-mean-and-median.png")

# ---------- Figure 5: waypoints ----------
route = [[0.0, 0.0], [2.0, 0.0], [2.0, 1.5], [4.0, 3.0]]
fig, ax = plt.subplots(figsize=(10.5, 6.8))
for g in range(0, 6):
    ax.plot([g, g], [-0.6, 3.7], color=L_GREY, lw=1, zorder=0)
for g in range(0, 4):
    ax.plot([-0.6, 5.0], [g, g], color=L_GREY, lw=1, zorder=0)
for i in range(3):
    a, b = route[i], route[i + 1]
    ax.add_patch(FancyArrowPatch(tuple(a), tuple(b), arrowstyle="-|>", mutation_scale=18, color=BLUE, lw=3, zorder=2))
for lab, xy in [("leg 1: 2.00 m", (1.0, -0.32)), ("leg 2: 1.50 m", (2.12, 0.75)), ("leg 3: 2.50 m", (3.15, 1.85))]:
    ax.text(*xy, lab, fontsize=12.5, color=BLUE, weight="bold", ha="left" if lab[4] != "1" else "center")
for i, (x, y) in enumerate(route):
    ax.plot(x, y, "o", color=ORANGE, ms=14, mec=BLACK, zorder=3)
    ax.text(x - 0.12, y + 0.17, f"route[{i}]", fontsize=11.5, family=MONO, ha="right")
ax.set_xlim(-1.2, 5.2); ax.set_ylim(-0.7, 3.8); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-waypoints.png")

# ---------- Figure 6: moving average ----------
readings = [10, 12, 9, 11, 30, 10, 12, 11, 9, 10]
sm = []
for i in range(len(readings)):
    w = readings[max(0, i - 2):i + 1]
    sm.append(sum(w) / len(w))
fig, ax = plt.subplots(figsize=(13, 5.0))
ax.plot(range(10), readings, "o-", color=GREY, lw=2, label="raw readings")
ax.plot(range(10), sm, "o-", color=BLUE, lw=3, label="moving average of 3")
ax.annotate("the spike is smaller, but it\nnow lasts for 3 readings", xy=(5, 17), xytext=(6.2, 24), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("reading number"); ax.set_ylabel("value"); ax.grid(alpha=0.3); ax.legend(loc="upper left", framealpha=1)
save(fig, "fig06-moving-average.png")
print("figures saved in", os.path.abspath(OUT))
