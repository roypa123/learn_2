# Figures for Chapter 23 — Functions part 1: making your own commands.
# Run:  python figures.py      (saves PNG files in ../../images/ch023/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch023")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw, connectionstyle=f"arc3,rad={rad}"))


def rbox(ax, x, y, w, h, text, face, size=12, family=None, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


# ---------- Figure 1: a function is a machine ----------
fig, ax = plt.subplots(figsize=(13.5, 5.2))
for i, (t, y) in enumerate([("value = 0.70", 3.2), ("low = -0.25", 2.3), ("high = 0.25", 1.4)]):
    ax.text(0.1, y, t, fontsize=13.5, family=MONO, weight="bold", va="center")
    arrow(ax, (2.9, y), (4.1, 2.3 + (y - 2.3) * 0.5), BLUE, 2.4)
rbox(ax, 4.15, 1.0, 4.4, 2.6, "clamp\n\nthe lines inside are\nhidden from the caller", L_ORANGE, 13.5, None, "bold")
arrow(ax, (8.6, 2.3), (10.1, 2.3), GREEN, 3)
ax.text(10.25, 2.3, "0.25", fontsize=20, family=MONO, weight="bold", va="center", color=GREEN)
ax.text(1.4, 4.0, "ARGUMENTS go in", fontsize=13, color=BLUE, weight="bold", ha="center")
ax.text(10.9, 3.1, "the RETURN value\ncomes out", fontsize=13, color=GREEN, weight="bold", ha="center")
ax.text(6.35, 0.25, "speed = clamp(0.70, -0.25, 0.25)", ha="center", fontsize=16, family=MONO, weight="bold")
ax.set_xlim(0, 12.8); ax.set_ylim(0, 4.4); ax.axis("off")
save(fig, "fig01-function-machine.png")

# ---------- Figure 2: flow of a call ----------
fig, ax = plt.subplots(figsize=(13.5, 6.4))
left = ["def double(n):", "    result = n * 2", "    return result", "", "", "a = 5", "b = double(a)", "print(b)"]
for i, t in enumerate(left):
    ax.text(0.5, 6.2 - i * 0.72, t, family=MONO, fontsize=15, va="center", weight="bold" if t.startswith("b =") else "normal")
ax.text(9.0, 6.0, "Python's order", fontsize=14, weight="bold", ha="center")
steps = ["1. reads the def: remembers it, runs nothing", "2. a = 5", "3. b = double(a): JUMPS into the function", "4. n = 5,  result = 10", "5. return: JUMPS back with 10", "6. b = 10", "7. print(b)  shows 10"]
for i, t in enumerate(steps):
    ax.text(6.3, 5.3 - i * 0.68, t, fontsize=12.5, va="center", color=(BLUE if i in (2, 3, 4) else BLACK))
ax.plot([5.2, 5.75, 5.75, 4.2], [1.87, 1.87, 5.48, 5.48], color=BLUE, lw=3)
arrow(ax, (4.2, 5.48), (4.0, 5.48), BLUE, 3)
ax.text(5.75, 1.45, "call", color=BLUE, fontsize=12.5, weight="bold", ha="center")
ax.plot([4.1, 4.75, 4.75], [4.76, 4.76, 2.25], color=GREEN, lw=3)
arrow(ax, (4.75, 2.25), (4.75, 1.95), GREEN, 3)
ax.text(4.75, 3.4, "return\n10", color=GREEN, fontsize=12.5, weight="bold", ha="center", va="center", bbox=dict(fc="white", ec="none", pad=1))
ax.set_xlim(0, 13.5); ax.set_ylim(0.6, 6.6); ax.axis("off")
save(fig, "fig02-flow-of-a-call.png")

# ---------- Figure 3: print and return ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 4.6))
for ax, code, verb, col, res, note in [
    (axes[0], ["def p(x):", "    print(x * 2)", "", "a = p(3)"], "shows 6 on the screen", RED, "a is None", "the value goes to a person's eyes.\nThe program cannot use it."),
    (axes[1], ["def r(x):", "    return x * 2", "", "b = r(3)"], "shows nothing", GREEN, "b is 6", "the value goes back to the program.\nIt can be stored and used.")]:
    for i, t in enumerate(code):
        ax.text(0.2, 4.0 - i * 0.62, t, family=MONO, fontsize=15, va="center")
    ax.text(5.0, 3.9, verb, fontsize=13, weight="bold", ha="left")
    ax.text(5.0, 2.95, res, fontsize=18, family=MONO, weight="bold", color=col)
    ax.text(0.2, 0.7, note, fontsize=12.5, va="center", style="italic")
    ax.set_xlim(0, 9.5); ax.set_ylim(0.1, 4.5); ax.axis("off")
save(fig, "fig03-print-and-return.png")

# ---------- Figure 4: the same lines many times, or one function ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6))
ax = axes[0]
ax.text(2.8, 6.95, "Copied lines", fontsize=14, weight="bold", color=RED, ha="center")
for k, y in enumerate((5.0, 3.1, 1.2)):
    ax.add_patch(Rectangle((0.5, y - 0.1), 4.6, 1.6, fc=L_RED, ec=BLACK))
    for i, t in enumerate(["if v > 0.25:", "    v = 0.25", "elif v < -0.25:", "    v = -0.25"]):
        ax.text(0.7, y + 1.25 - i * 0.37, t.replace("v", "vls"[k]), family=MONO, fontsize=10.5, va="center")
ax.text(2.8, 0.5, "a bug must be fixed in 3 places", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0, 5.6); ax.set_ylim(0.2, 7.3); ax.axis("off")
ax = axes[1]
ax.text(3.0, 6.95, "One function, used 3 times", fontsize=14, weight="bold", color=GREEN, ha="center")
rbox(ax, 0.5, 4.2, 5.0, 1.6, "def clamp(value, low, high):\n    ...\n    return value", L_GREEN, 12.5, MONO)
for i, t in enumerate(["v = clamp(v, -0.25, 0.25)", "l = clamp(l, -0.25, 0.25)", "s = clamp(s, 0, 100)"]):
    ax.text(0.5, 3.3 - i * 0.72, t, family=MONO, fontsize=13, va="center")
    arrow(ax, (5.3, 3.3 - i * 0.72), (5.75, 4.3), GREEN, 1.6, rad=0.3)
ax.text(3.0, 0.5, "a bug is fixed in 1 place, and everything is fixed", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0, 6.4); ax.set_ylim(0.2, 7.3); ax.axis("off")
save(fig, "fig04-copies-or-function.png")
print("figures saved in", os.path.abspath(OUT))
