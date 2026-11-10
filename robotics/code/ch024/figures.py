# Figures for Chapter 24 — Functions part 2: parameters, return values, scope.
# Run:  python figures.py      (saves PNG files in ../../images/ch024/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch024")
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


def chip(ax, x, y, text, face=L_ORANGE, w=2.3):
    ax.add_patch(FancyBboxPatch((x, y), w, 0.55, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK))
    ax.text(x + w / 2, y + 0.27, text, ha="center", va="center", fontsize=12.5, family=MONO, weight="bold")


# ---------- Figure 1: scope ----------
fig, ax = plt.subplots(figsize=(13.5, 6.0))
ax.add_patch(Rectangle((0.2, 0.3), 13, 5.3, fc=L_BLUE, ec=BLACK, lw=1.8, alpha=0.5))
ax.text(0.45, 5.25, "GLOBAL: the main program", fontsize=13.5, weight="bold", color=BLUE)
chip(ax, 0.6, 4.4, "speed = 0.2", L_BLUE)
ax.add_patch(Rectangle((3.6, 0.8), 4.3, 3.9, fc=L_ORANGE, ec=BLACK, lw=1.8, alpha=0.7))
ax.text(5.75, 4.32, "inside drive()", ha="center", fontsize=13, weight="bold")
chip(ax, 4.6, 3.3, "t = 8")
chip(ax, 4.6, 2.3, "metres = 1.6")
ax.add_patch(Rectangle((8.5, 0.8), 4.3, 3.9, fc=L_GREEN, ec=BLACK, lw=1.8, alpha=0.7))
ax.text(10.65, 4.32, "inside brake()", ha="center", fontsize=13, weight="bold")
chip(ax, 9.5, 3.3, "t = 2", L_GREEN)
chip(ax, 9.5, 2.3, "speed = 0.9", L_GREEN)
ax.text(5.75, 1.5, "can READ speed\nfrom outside", ha="center", va="center", fontsize=12, color=BLUE, weight="bold")
ax.text(10.65, 1.5, "its own speed: the\noutside one is untouched", ha="center", va="center", fontsize=12, color=RED, weight="bold")
ax.text(1.75, 2.6, "the main program\ncannot see inside\neither function", ha="center", va="center", fontsize=12)
ax.set_xlim(0, 13.4); ax.set_ylim(0.1, 5.8); ax.axis("off")
save(fig, "fig01-scope.png")

# ---------- Figure 2: a local variable lives only during the call ----------
fig, ax = plt.subplots(figsize=(13, 3.8))
ax.plot([0, 12], [1, 1], color=BLACK, lw=2)
ax.text(12.1, 1, "time", va="center", fontsize=12)
for a, b, y, c, t in [(2.6, 5.8, 2.0, L_ORANGE, "first call: secret exists"), (7.6, 10.8, 2.0, L_ORANGE, "second call: a NEW secret")]:
    ax.add_patch(Rectangle((a, 1), b - a, y - 1, fc=c, ec=BLACK, lw=1.3))
    ax.text((a + b) / 2, 1.5, t, ha="center", va="center", fontsize=11)
for x, lab in [(2.6, "call"), (5.8, "return"), (7.6, "call"), (10.8, "return")]:
    ax.plot([x, x], [0.75, 1.0], color=BLACK, lw=1.5)
    ax.text(x, 0.45, lab, ha="center", fontsize=12)
ax.text(6.6, 2.55, "between calls, and after them, the local variable does not exist", ha="center", fontsize=13, weight="bold")
ax.set_xlim(0, 13); ax.set_ylim(0.2, 2.9); ax.axis("off")
save(fig, "fig02-local-lifetime.png")

# ---------- Figure 3: numbers and lists as parameters ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.0))
ax = axes[0]
ax.text(3.2, 5.4, "A number: the name inside moves", ha="center", fontsize=14, weight="bold", color=BLUE)
for i, t in enumerate(["def f(n):", "    n = n + 1", "a = 5", "f(a)      # a is still 5"]):
    ax.text(0.2, 4.6 - i * 0.5, t, family=MONO, fontsize=12.5, va="center")
chip(ax, 0.6, 1.9, "a", L_BLUE, 0.9); chip(ax, 3.9, 1.9, "n", L_ORANGE, 0.9)
ax.add_patch(Rectangle((0.6, 0.6), 0.9, 0.7, fc="white", ec=BLACK)); ax.text(1.05, 0.95, "5", ha="center", va="center", fontsize=14, family=MONO)
ax.add_patch(Rectangle((3.9, 0.6), 0.9, 0.7, fc="white", ec=BLACK)); ax.text(4.35, 0.95, "6", ha="center", va="center", fontsize=14, family=MONO)
arrow(ax, (1.05, 1.88), (1.05, 1.32), ORANGE); arrow(ax, (4.35, 1.88), (4.35, 1.32), ORANGE)
ax.set_xlim(0, 6.4); ax.set_ylim(0.3, 5.8); ax.axis("off")
ax = axes[1]
ax.text(3.2, 5.4, "A list: both names share one list", ha="center", fontsize=14, weight="bold", color=RED)
for i, t in enumerate(["def f(m):", "    m.append(9)", "x = [1]", "f(x)      # x is now [1, 9]"]):
    ax.text(0.2, 4.6 - i * 0.5, t, family=MONO, fontsize=12.5, va="center")
chip(ax, 1.0, 1.9, "x", L_BLUE, 0.9); chip(ax, 4.2, 1.9, "m", L_ORANGE, 0.9)
for i, v in enumerate(["1", "9"]):
    ax.add_patch(Rectangle((2.3 + i * 0.9, 0.6), 0.9, 0.7, fc=L_ORANGE if i else "white", ec=BLACK))
    ax.text(2.75 + i * 0.9, 0.95, v, ha="center", va="center", fontsize=14, family=MONO)
arrow(ax, (1.5, 1.88), (2.5, 1.33), ORANGE); arrow(ax, (4.6, 1.88), (3.9, 1.33), ORANGE)
ax.set_xlim(0, 6.4); ax.set_ylim(0.3, 5.8); ax.axis("off")
save(fig, "fig03-numbers-and-lists-as-parameters.png")

# ---------- Figure 4: ways to pass arguments ----------
fig, ax = plt.subplots(figsize=(13.5, 5.4))
ax.text(6.7, 5.2, "def plan_trip(route, speed_ms=0.25, power_w=3.78):", ha="center", fontsize=15, family=MONO, weight="bold")
params = [("route", 1.0), ("speed_ms", 5.3), ("power_w", 9.8)]
for name, x in params:
    chip(ax, x, 4.05, name, L_ORANGE, 2.5)
rows = [("plan_trip(r)", ["r", "0.25 (default)", "3.78 (default)"], 3.0),
        ("plan_trip(r, 0.5)", ["r", "0.5", "3.78 (default)"], 2.0),
        ("plan_trip(r, power_w=8.78)", ["r", "0.25 (default)", "8.78"], 1.0)]
for code, vals, y in rows:
    for (name, x), v in zip(params, vals):
        ax.text(x + 1.25, y, v, ha="center", va="center", fontsize=12.5, family=MONO, color=GREY if "default" in v else BLUE, weight="bold")
    ax.text(6.7, y - 0.42, code, ha="center", fontsize=12.5, family=MONO)
ax.set_xlim(0.5, 13); ax.set_ylim(0.3, 5.6); ax.axis("off")
save(fig, "fig04-passing-arguments.png")
print("figures saved in", os.path.abspath(OUT))
