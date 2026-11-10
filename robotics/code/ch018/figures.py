# Figures for Chapter 18 — Making decisions: if, elif, else.
# Run:  python figures.py      (saves PNG files in ../../images/ch018/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch018")
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


def diamond(ax, cx, cy, w, h, text, size=11.5):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True,
                         fc=L_ORANGE, ec=BLACK, lw=1.3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, family=MONO)


def code_lines(ax, x, y, lines, size=14, dy=0.62):
    for i, (t, c) in enumerate(lines):
        ax.text(x, y - i * dy, t, family=MONO, fontsize=size, color=c, va="center", weight="bold")


# ---------- Figure 1: the parts of an if statement ----------
fig, ax = plt.subplots(figsize=(13.5, 5.2))
ax.add_patch(Rectangle((1.9, 1.45), 7.3, 1.25, fc=L_GREEN, ec="none"))
ax.add_patch(Rectangle((1.3, 1.45), 0.6, 1.25, fc=L_ORANGE, ec="none"))
code_lines(ax, 1.35, 3.0, [("if distance_m < 0.3:", BLACK), ("    print(\"wall!\")", BLACK), ("    speed_ms = 0.0", BLACK),
                           ("print(\"loop done\")", BLACK)], 18, 0.62)
ax.annotate("the word if", xy=(1.55, 3.2), xytext=(0.2, 4.2), fontsize=12, arrowprops=dict(arrowstyle="-|>", color=GREY))
ax.annotate("a condition: True or False\n(Chapter 17)", xy=(4.7, 3.22), xytext=(3.6, 4.15), fontsize=12, arrowprops=dict(arrowstyle="-|>", color=GREY))
ax.annotate("the colon: never forget it", xy=(5.3, 3.12), xytext=(8.3, 4.2), fontsize=12, color=RED, weight="bold",
            arrowprops=dict(arrowstyle="-|>", color=RED))
ax.text(9.5, 2.1, "the BLOCK: these lines\nrun only when the\ncondition is True", fontsize=12.5, color=GREEN, weight="bold", va="center")
ax.text(1.0, 0.2, "4 spaces: the indentation marks the block (orange strip).", fontsize=12.5, color=ORANGE, weight="bold")
ax.text(9.5, 1.14, "not indented: always runs", fontsize=12.5, va="center")
arrow(ax, (9.45, 1.14), (5.6, 1.14), GREY, 1.5)
ax.set_xlim(0, 13.5); ax.set_ylim(0, 4.6); ax.axis("off")
save(fig, "fig01-parts-of-if.png")

# ---------- Figure 2: if / else flowchart ----------
fig, ax = plt.subplots(figsize=(13, 6.8))
rbox(ax, 4.6, 6.1, 3.6, 0.7, "distance_m = ... sensor", L_GREY, 12, MONO)
arrow(ax, (6.4, 6.08), (6.4, 5.5))
diamond(ax, 6.4, 4.5, 5.2, 2.0, "distance_m < 0.3 ?", 13)
arrow(ax, (3.8, 4.5), (1.9, 4.5)); arrow(ax, (1.9, 4.5), (1.9, 3.0))
arrow(ax, (9.0, 4.5), (10.9, 4.5)); arrow(ax, (10.9, 4.5), (10.9, 3.0))
ax.text(2.9, 4.72, "True", fontsize=13, weight="bold", color=GREEN, ha="center")
ax.text(9.95, 4.72, "False", fontsize=13, weight="bold", color=RED, ha="center")
rbox(ax, 0.2, 1.9, 3.4, 1.05, "if block:\nspeed_ms = 0.0", L_GREEN, 12.5, MONO)
rbox(ax, 9.2, 1.9, 3.4, 1.05, "else block:\nspeed_ms = 0.25", L_BLUE, 12.5, MONO)
ax.plot([1.9, 1.9], [1.88, 1.2], color=BLACK, lw=2); ax.plot([10.9, 10.9], [1.88, 1.2], color=BLACK, lw=2)
ax.plot([1.9, 10.9], [1.2, 1.2], color=BLACK, lw=2)
arrow(ax, (6.4, 1.2), (6.4, 0.72))
rbox(ax, 4.2, 0.0, 4.4, 0.7, "the program continues here", L_GREY, 12)
ax.text(6.4, 2.45, "exactly ONE of the\ntwo blocks runs", ha="center", va="center", fontsize=13, style="italic")
ax.set_xlim(0, 12.9); ax.set_ylim(-0.1, 7.0); ax.axis("off")
save(fig, "fig02-if-else-flowchart.png")

# ---------- Figure 3: elif and voltage bands ----------
fig, axes = plt.subplots(2, 1, figsize=(13, 6.4), gridspec_kw={"height_ratios": [1, 1.3]})
ax = axes[0]
bands = [(3.2, 3.5, L_RED, "LAND NOW"), (3.5, 3.7, L_ORANGE, "RETURN HOME"), (3.7, 4.3, L_GREEN, "NORMAL")]
for a, b, c, t in bands:
    ax.add_patch(Rectangle((a, 0), b - a, 1, fc=c, ec=BLACK))
    ax.text((a + b) / 2, 0.5, t, ha="center", va="center", fontsize=13.5, weight="bold")
for v in (3.2, 3.5, 3.7, 4.0, 4.2):
    ax.plot([v, v], [-0.12, 0], color=BLACK, lw=1.5)
    ax.text(v, -0.38, f"{v:.1f}", ha="center", fontsize=12, family=MONO)
ax.text(3.75, -0.82, "volts per cell", ha="center", fontsize=12)
ax.set_xlim(3.15, 4.35); ax.set_ylim(-1.0, 1.2); ax.axis("off")
ax = axes[1]
ax.text(0.01, 0.97, "Right: highest test first", transform=ax.transAxes, fontsize=14, weight="bold", color=GREEN, va="top")
ax.text(0.53, 0.97, "Wrong: 3.5 is tested first", transform=ax.transAxes, fontsize=14, weight="bold", color=RED, va="top")
right = ["if v >= 3.7:", "    action = 'normal'", "elif v >= 3.5:", "    action = 'return home'", "else:", "    action = 'land now'"]
wrong = ["if v >= 3.5:", "    action = 'return home'", "elif v >= 3.7:", "    action = 'normal'    # never runs!", "else:", "    action = 'land now'"]
for j, t in enumerate(right):
    ax.text(0.02, 0.8 - j * 0.14, t, transform=ax.transAxes, family=MONO, fontsize=13, va="top")
for j, t in enumerate(wrong):
    ax.text(0.54, 0.8 - j * 0.14, t, transform=ax.transAxes, family=MONO, fontsize=13, va="top",
            color=RED if j == 3 else BLACK)
ax.axis("off")
save(fig, "fig03-elif-voltage-bands.png")

# ---------- Figure 4: which lines belong to the block ----------
fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.6))
for ax, title, lines, shade, out in [
    (axes[0], "Both lines are in the block", ["if battery < 2:", "    print('low')", "    print('charge me')", "print('end')"], (1, 2), "battery = 5 prints:\nend"),
    (axes[1], "Only ONE line is in the block", ["if battery < 2:", "    print('low')", "print('charge me')", "print('end')"], (1, 1), "battery = 5 prints:\ncharge me\nend")]:
    ax.text(0.2, 4.6, title, fontsize=14, weight="bold")
    y0 = 3.9
    a, b = shade
    ax.add_patch(Rectangle((0.1, y0 - b * 0.7 - 0.33), 6.9, (b - a + 1) * 0.7, fc=L_GREEN, ec="none"))
    for i, t in enumerate(lines):
        ax.text(0.2, y0 - i * 0.7, t, family=MONO, fontsize=13, va="center", weight="bold")
    ax.text(7.4, 2.9, out, fontsize=12.5, family=MONO, va="center",
            bbox=dict(boxstyle="round,pad=0.5", fc="#1E1E1E", ec=BLACK), color="#B5E8B0")
    ax.set_xlim(0, 12.2); ax.set_ylim(0.9, 5); ax.axis("off")
save(fig, "fig04-which-lines-are-in-the-block.png")

# ---------- Figure 5: speed command against distance ----------
SP, GAIN, MAXV, DB = 0.30, 1.0, 0.25, 0.01
ds = [i / 2000 for i in range(0, 1601)]


def cmd(d):
    e = d - SP
    v = 0.0 if abs(e) < DB else GAIN * e
    return max(-MAXV, min(MAXV, v))


fig, ax = plt.subplots(figsize=(13, 5.6))
ax.plot(ds, [cmd(d) for d in ds], color=GREEN, lw=3, label="speed command")
ax.plot(ds, [GAIN * (d - SP) for d in ds], color=GREY, lw=1.5, ls=":", label="no limits: gain x error")
ax.axvline(SP, color=BLACK, ls="--", lw=2, label="setpoint 0.30 m")
ax.axhline(0, color=GREY, lw=1)
ax.annotate("clamp: never above +0.25", xy=(0.68, 0.25), xytext=(0.5, 0.33), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("clamp: never below -0.25", xy=(0.02, -0.25), xytext=(0.09, -0.34), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("deadband: within 1 cm,\nthe command is 0", xy=(0.305, 0.0), xytext=(0.36, -0.2), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("distance to the wall (m)"); ax.set_ylabel("speed command (m/s)")
ax.set_xlim(0, 0.8); ax.set_ylim(-0.4, 0.4); ax.grid(alpha=0.3); ax.legend(loc="lower right", framealpha=1)
save(fig, "fig05-clamp-and-deadband.png")
print("figures saved in", os.path.abspath(OUT))
