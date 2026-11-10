# Figures for Chapter 22 — Tuples and dictionaries.
# Run:  python figures.py      (saves PNG files in ../../images/ch022/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch022")
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


def rbox(ax, x, y, w, h, text, face, size=12, family=None, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


# ---------- Figure 1: three containers ----------
fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))
ax = axes[0]
ax.text(2.4, 3.6, "list  [ ]", ha="center", fontsize=15, weight="bold", family=MONO, color=BLUE)
for i, v in enumerate(["0.52", "0.51", "0.53"]):
    ax.add_patch(Rectangle((0.3 + i * 1.4, 1.6), 1.4, 1.0, fc=L_BLUE, ec=BLACK, lw=1.4))
    ax.text(1.0 + i * 1.4, 2.1, v, ha="center", va="center", fontsize=13, family=MONO, weight="bold")
    ax.text(1.0 + i * 1.4, 2.85, str(i), ha="center", fontsize=12, color=BLUE, weight="bold")
ax.text(2.4, 0.9, "found by POSITION\ncan change, can grow", ha="center", va="center", fontsize=12.5)
ax.set_xlim(0, 4.8); ax.set_ylim(0.3, 4); ax.axis("off")
ax = axes[1]
ax.text(2.4, 3.6, "tuple  ( )", ha="center", fontsize=15, weight="bold", family=MONO, color=ORANGE)
for i, v in enumerate(["2.0", "1.5"]):
    ax.add_patch(Rectangle((1.0 + i * 1.4, 1.6), 1.4, 1.0, fc=L_ORANGE, ec=BLACK, lw=1.4))
    ax.text(1.7 + i * 1.4, 2.1, v, ha="center", va="center", fontsize=13, family=MONO, weight="bold")
    ax.text(1.7 + i * 1.4, 2.85, str(i), ha="center", fontsize=12, color=ORANGE, weight="bold")
ax.add_patch(Rectangle((0.9, 1.5), 3.0, 1.2, fc="none", ec=RED, lw=3))
ax.text(2.4, 0.9, "found by POSITION\nlocked: cannot change", ha="center", va="center", fontsize=12.5)
ax.set_xlim(0, 4.8); ax.set_ylim(0.3, 4); ax.axis("off")
ax = axes[2]
ax.text(2.4, 3.6, "dict  { }", ha="center", fontsize=15, weight="bold", family=MONO, color=GREEN)
for i, (k, v) in enumerate([("\"wheels\"", "2"), ("\"speed\"", "0.25")]):
    y = 2.3 - i * 0.75
    ax.add_patch(Rectangle((0.3, y), 2.3, 0.65, fc=L_GREEN, ec=BLACK, lw=1.4))
    ax.add_patch(Rectangle((2.6, y), 1.9, 0.65, fc="white", ec=BLACK, lw=1.4))
    ax.text(1.45, y + 0.32, k, ha="center", va="center", fontsize=12.5, family=MONO, weight="bold")
    ax.text(3.55, y + 0.32, v, ha="center", va="center", fontsize=13, family=MONO, weight="bold")
ax.text(2.4, 0.9, "found by NAME (the key)\ncan change, can grow", ha="center", va="center", fontsize=12.5)
ax.set_xlim(0, 4.8); ax.set_ylim(0.3, 4); ax.axis("off")
save(fig, "fig01-three-containers.png")

# ---------- Figure 2: a dictionary looks up by key ----------
fig, ax = plt.subplots(figsize=(13, 5.0))
items = [("\"name\"", "'Rover'"), ("\"wheels\"", "2"), ("\"max_speed_ms\"", "0.5"), ("\"battery_wh\"", "11.52")]
for i, (k, v) in enumerate(items):
    y = 3.6 - i * 0.95
    c = L_ORANGE if i == 2 else L_GREEN
    ax.add_patch(Rectangle((5.0, y), 3.6, 0.8, fc=c, ec=BLACK, lw=1.4))
    ax.add_patch(Rectangle((8.6, y), 2.4, 0.8, fc=c if i == 2 else "white", ec=BLACK, lw=1.4))
    ax.text(6.8, y + 0.4, k, ha="center", va="center", fontsize=13.5, family=MONO, weight="bold")
    ax.text(9.8, y + 0.4, v, ha="center", va="center", fontsize=14, family=MONO, weight="bold")
ax.text(6.8, 4.65, "keys", ha="center", fontsize=13, weight="bold", color=GREEN)
ax.text(9.8, 4.65, "values", ha="center", fontsize=13, weight="bold")
ax.text(0.1, 2.05, 'config["max_speed_ms"]', fontsize=14, family=MONO, weight="bold", va="center")
arrow(ax, (3.9, 2.05), (4.95, 2.05), ORANGE, 3)
arrow(ax, (11.05, 2.05), (11.8, 2.05), ORANGE, 3)
ax.text(11.9, 2.05, "0.5", fontsize=18, family=MONO, weight="bold", va="center", color=BLUE)
ax.text(6.5, 0.2, "You give the key, and Python goes straight to its value. No searching by position.", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis("off")
save(fig, "fig02-lookup-by-key.png")

# ---------- Figure 3: if chain against table ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6))
ax = axes[0]
ax.text(0.1, 7.3, "A long if / elif chain", fontsize=14, weight="bold", color=RED)
lines = ['if word == "forward":', "    left, right = 1.0, 1.0", 'elif word == "back":', "    left, right = -1.0, -1.0", 'elif word == "left":',
         "    left, right = -0.5, 0.5", 'elif word == "right":', "    left, right = 0.5, -0.5"]
for i, t in enumerate(lines):
    ax.text(0.1, 6.4 - i * 0.8, t, family=MONO, fontsize=12.5, va="center")
ax.set_xlim(0, 7); ax.set_ylim(0, 7.8); ax.axis("off")
ax = axes[1]
ax.text(0.1, 7.3, "A table (data) and one line of code", fontsize=14, weight="bold", color=GREEN)
lines = ["COMMANDS = {", '    "forward": (1.0, 1.0),', '    "back":    (-1.0, -1.0),', '    "left":    (-0.5, 0.5),', '    "right":   (0.5, -0.5),', "}", "", "left, right = COMMANDS[word]"]
for i, t in enumerate(lines):
    ax.text(0.1, 6.4 - i * 0.8, t, family=MONO, fontsize=12.5, va="center", weight="bold" if i == 7 else "normal", color=GREEN if i == 7 else BLACK)
ax.set_xlim(0, 7); ax.set_ylim(0, 7.8); ax.axis("off")
save(fig, "fig03-chain-or-table.png")


# ---------- Figure 4: wheel commands ----------
def rover(ax, cx, title, left, right):
    ax.add_patch(FancyBboxPatch((cx - 0.7, 0.8), 1.4, 1.8, boxstyle="round,pad=0.02,rounding_size=0.15", fc=L_ORANGE, ec=BLACK, lw=1.4))
    ax.add_patch(Polygon([(cx, 2.9), (cx - 0.28, 2.45), (cx + 0.28, 2.45)], closed=True, fc=ORANGE, ec=BLACK))
    for sx, v in [(-0.95, left), (0.95, right)]:
        ax.add_patch(Rectangle((cx + sx - 0.14, 1.3), 0.28, 0.8, fc=BLACK))
        if v != 0:
            ln = 0.85 * abs(v)
            s = 1 if v > 0 else -1
            arrow(ax, (cx + sx, 1.7), (cx + sx, 1.7 + s * (0.5 + ln)), GREEN, 3)
    ax.text(cx, 3.95, title, ha="center", fontsize=14, family=MONO, weight="bold")
    ax.text(cx, 0.05, f"({left}, {right})", ha="center", fontsize=12, family=MONO)


fig, ax = plt.subplots(figsize=(14, 4.8))
for i, (t, l, r) in enumerate([("forward", 1.0, 1.0), ("back", -1.0, -1.0), ("left", -0.5, 0.5), ("right", 0.5, -0.5), ("stop", 0.0, 0.0)]):
    rover(ax, 1.6 + i * 3.0, t, l, r)
ax.set_xlim(0, 15); ax.set_ylim(-0.2, 4.3); ax.axis("off")
save(fig, "fig04-wheel-commands.png")

# ---------- Figure 5: joint limits ----------
limits = {"left_hip": (-30, 90), "left_knee": (0, 135), "left_ankle": (-40, 25), "right_hip": (-30, 90), "right_knee": (0, 135), "right_ankle": (-40, 25)}
pose = {"left_hip": 45, "left_knee": 140, "left_ankle": -10, "right_hip": 20, "right_knee": 30, "right_ankle": 31}
fig, ax = plt.subplots(figsize=(13, 5.4))
names = list(limits)
for i, n in enumerate(names):
    y = len(names) - 1 - i
    lo, hi = limits[n]
    ax.barh(y, hi - lo, left=lo, height=0.55, color=L_GREEN, ec=BLACK)
    a = pose[n]
    bad = a < lo or a > hi
    ax.plot(a, y, "D", color=RED if bad else BLUE, ms=11, mec=BLACK, zorder=5)
    if bad:
        ax.text(a + 4, y, f"{a}: too far", va="center", fontsize=12, color=RED, weight="bold")
ax.set_yticks(range(len(names))); ax.set_yticklabels(names[::-1], family=MONO)
ax.set_xlabel("joint angle (degrees)"); ax.grid(axis="x", alpha=0.3); ax.set_xlim(-60, 185)
ax.add_patch(Rectangle((0, 0), 0, 0, fc=L_GREEN, ec=L_GREEN, label="safe range (from the dictionary)"))
ax.plot([], [], "D", color=BLUE, mec=BLACK, label="requested angle: fine")
ax.plot([], [], "D", color=RED, mec=BLACK, label="requested angle: outside")
ax.legend(loc="lower right", framealpha=1)
save(fig, "fig05-joint-limits.png")
print("figures saved in", os.path.abspath(OUT))
