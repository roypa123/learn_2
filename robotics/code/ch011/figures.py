# Figures for Chapter 11 — What is a program? Instructions in order.
# Run:  python figures.py      (saves PNG files in ../../images/ch011/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch011")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11, family=None, ha="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    tx = x + w / 2 if ha == "center" else x + 0.15
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=size, family=family)


def arrow(ax, p, q, colour=GREY, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


# ---------- Figure 1: a recipe and a program ----------
fig, ax = plt.subplots(figsize=(14, 4.6))
box(ax, 0.0, 0.3, 5.6, 3.4, "MAKE A SANDWICH\n\n1. Take two slices of bread.\n2. Spread butter on one slice.\n"
    "3. Put cheese on the butter.\n4. Put the other slice on top.\n5. Cut it in half.", L_ORANGE, 12.5, ha="left")
box(ax, 8.2, 0.3, 5.8, 3.4, "PICK UP A BLOCK (robot arm)\n\n1. Open the gripper.\n2. Move down to the block.\n"
    "3. Close the gripper.\n4. Lift.\n5. Move to the box and open.", L_BLUE, 12.5, ha="left")
arrow(ax, (5.8, 2.2), (8.0, 2.2), BLACK, 2.5)
arrow(ax, (8.0, 1.8), (5.8, 1.8), BLACK, 2.5)
ax.text(6.9, 2.6, "the same idea:", ha="center", fontsize=11.5, style="italic")
ax.text(6.9, 1.0, "instructions,\none at a time,\nin order", ha="center", fontsize=12, weight="bold")
ax.text(7.0, 4.25, "A recipe and a robot program are both lists of instructions in order", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-0.2, 14.2); ax.set_ylim(0, 4.6); ax.axis("off")
save(fig, "fig01-recipe-and-program.png")

# ---------- Figure 2: the same moves in two orders ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 6.4))
paths = {"A": [(0, 0), (3, 0), (3, 2), (4, 2), (4, 3)], "B": [(0, 0), (0, 2), (3, 2), (3, 3), (4, 3)]}
titles = {"A": "grid_trip.py: 3 east, 2 north, 1 east, 1 north",
          "B": "grid_trip_b.py: 2 north, 3 east, 1 north, 1 east"}
for ax, key, col in [(axes[0], "A", BLUE), (axes[1], "B", RED)]:
    for gx in range(6):
        for gy in range(5):
            ax.add_patch(Rectangle((gx - 0.5, gy - 0.5), 1, 1, fc="white", ec=L_GREY, lw=1))
    for ox in (1, 2):
        ax.add_patch(Rectangle((ox - 0.5, 1.5), 1, 1, fc=GREY, ec=BLACK))
    ax.text(1.5, 1.72, "TABLE", ha="center", va="center", fontsize=11, color="white", weight="bold")
    p = paths[key]
    ax.plot([q[0] for q in p], [q[1] for q in p], color=col, lw=4, marker="o", ms=9, zorder=3)
    for i, q in enumerate(p[1:], start=1):
        ax.text(q[0] + 0.12, q[1] + 0.18, str(i), fontsize=11, weight="bold", color=col, zorder=4)
    ax.add_patch(Rectangle((-0.35, -0.35), 0.7, 0.7, fc=ORANGE, ec=BLACK, zorder=2))
    ax.text(0, -0.75, "start (0, 0)", ha="center", fontsize=10.5)
    ax.plot(4, 3, marker="*", color=GREEN, ms=26, zorder=5)
    ax.text(4, 3.55, "goal (4, 3)", ha="center", fontsize=10.5)
    ax.set_xlim(-0.8, 5.6); ax.set_ylim(-1.0, 4.6); ax.set_aspect("equal")
    ax.set_xticks(range(6)); ax.set_yticks(range(5)); ax.set_xlabel("x (east)"); ax.set_ylabel("y (north)")
    ax.set_title(titles[key], fontsize=11.5)
axes[0].set_title(titles["A"] + "\nreaches the goal safely", fontsize=11.5, color=BLUE)
axes[1].set_title(titles["B"] + "\nsame moves, same goal... but drives THROUGH the table", fontsize=11.5, color=RED)
save(fig, "fig02-two-orders-on-a-grid.png")

# ---------- Figure 3: a flowchart of a sequence ----------
fig, ax = plt.subplots(figsize=(7.5, 10))
ax.add_patch(Ellipse((2.5, 11.2), 2.4, 0.9, fc=L_GREEN, ec=BLACK, lw=1.3)); ax.text(2.5, 11.2, "START", ha="center", va="center", weight="bold")
steps = ["x = 0, y = 0", "move 3 east\n(x = x + 3)", "move 2 north\n(y = y + 2)", "move 1 east\n(x = x + 1)", "move 1 north\n(y = y + 1)"]
ys = [9.6, 8.0, 6.4, 4.8, 3.2]
for t, yy in zip(steps, ys):
    box(ax, 0.9, yy - 0.5, 3.2, 1.0, t, L_BLUE, 11.5)
ax.add_patch(Ellipse((2.5, 1.6), 2.4, 0.9, fc=L_RED, ec=BLACK, lw=1.3)); ax.text(2.5, 1.6, "END", ha="center", va="center", weight="bold")
pts = [11.2 - 0.45] + [v for yy in ys for v in (yy + 0.5, yy - 0.5)] + [1.6 + 0.45]
for i in range(0, len(pts), 2):
    arrow(ax, (2.5, pts[i]), (2.5, pts[i + 1]), BLACK, 1.8)
ax.text(4.4, 11.2, "oval = start / end", fontsize=10.5, va="center")
ax.text(4.4, 9.6, "rectangle = one\ninstruction", fontsize=10.5, va="center")
ax.text(4.4, 6.4, "arrows = the order:\nalways one way,\ntop to bottom", fontsize=10.5, va="center")
ax.set_xlim(0, 7.2); ax.set_ylim(1.0, 11.8); ax.axis("off")
ax.set_title("A flowchart of grid_trip.py", fontsize=13)
save(fig, "fig03-flowchart-sequence.png")


# ---------- Figure 4: pick and place, right and wrong order ----------
def frame(ax, x0, z, gripper, holding, label, ok=True):
    ax.add_patch(Rectangle((x0, 0), 2.2, 0.15, fc=GREY, ec=BLACK))                 # table
    if not holding:
        ax.add_patch(Rectangle((x0 + 0.85, 0.15), 0.5, 0.5, fc=GREEN, ec=BLACK))   # block on the table
    top = 0.15 + 0.5 + z * 0.12
    ax.plot([x0 + 1.1, x0 + 1.1], [top + 0.35, 3.0], color=ORANGE, lw=6)         # arm
    gap = 0.32 if gripper == "open" else 0.26
    for s in (-1, 1):
        ax.plot([x0 + 1.1 + s * gap, x0 + 1.1 + s * gap], [top - 0.5, top + 0.35], color=BLACK, lw=4)
    ax.plot([x0 + 1.1 - gap, x0 + 1.1 + gap], [top + 0.35, top + 0.35], color=BLACK, lw=4)
    if holding:
        ax.add_patch(Rectangle((x0 + 0.85, top - 0.5), 0.5, 0.5, fc=GREEN, ec=BLACK))
    ax.text(x0 + 1.1, -0.45, label, ha="center", va="top", fontsize=10.5, color=BLACK if ok else RED)


fig, axes = plt.subplots(2, 1, figsize=(14, 8.4))
right = [(10, "open", False, "start"), (0, "open", False, "1. move down"), (0, "closed", True, "2. close"),
         (10, "closed", True, "3. lift: holding True")]
wrong = [(10, "open", False, "start"), (10, "closed", False, "2. close (too early!)"), (0, "closed", False, "1. move down"),
         (10, "closed", False, "3. lift: holding False")]
for ax, seq, title, col in [(axes[0], right, "pick_place.py: the right order", GREEN),
                            (axes[1], wrong, "pick_place_wrong.py: two steps swapped", RED)]:
    for i, (z, g, h, lab) in enumerate(seq):
        frame(ax, i * 3.2, z, g, h, lab, ok=(col == GREEN or i == 0))
        if i < 3:
            arrow(ax, (i * 3.2 + 2.3, 1.5), (i * 3.2 + 3.1, 1.5), GREY, 1.8)
    ax.set_title(title, fontsize=13, color=col, weight="bold")
    ax.set_xlim(-0.2, 12.6); ax.set_ylim(-1.2, 3.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-pick-and-place-order.png")

# ---------- Figure 5: Python reads top to bottom (a trace) ----------
fig, ax = plt.subplots(figsize=(13, 5.4))
lines = ["battery = 80", "battery = battery + 20", "battery = battery / 2", 'print("...", battery, "%")']
values = ["80", "100", "50.0", "(prints 50.0)"]
for i, (ln, v) in enumerate(zip(lines, values)):
    y = 4.0 - i * 1.1
    ax.text(0.2, y, f"line {i + 2}", fontsize=11, color=GREY, va="center")
    box(ax, 1.4, y - 0.4, 5.4, 0.8, ln, "white", 12, MONO, ha="left")
    arrow(ax, (6.9, y), (8.1, y), BLUE, 1.8)
    box(ax, 8.2, y - 0.4, 2.2, 0.8, v, L_ORANGE if i < 3 else L_GREY, 12.5, MONO)
ax.annotate("", xy=(1.1, 0.5), xytext=(1.1, 4.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3))
ax.text(10.7, 4.0, "<- the box 'battery'\n    after each line", fontsize=11, va="center")
ax.text(5.6, 4.85, "Python runs ONE line at a time, from top to bottom", ha="center", fontsize=13, weight="bold")
ax.text(0.6, 0.15, "order", color=RED, fontsize=11, weight="bold")
ax.set_xlim(0, 13.2); ax.set_ylim(-0.1, 5.2); ax.axis("off")
save(fig, "fig05-top-to-bottom-trace.png")
print("figures saved in", os.path.abspath(OUT))
