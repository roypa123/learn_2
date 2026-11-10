# Figures for Chapter 16 — Output and input: print and input.
# Run:  python figures.py      (saves PNG files in ../../images/ch016/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch016")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
TERM_BG, TERM_FG, OUTC = "#1E1E1E", "#F0F0F0", "#B5E8B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=GREY, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw))


def rbox(ax, x, y, w, h, text, face, size=12, family=None, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


# ---------- Figure 1: how print builds its line ----------
fig, ax = plt.subplots(figsize=(13.5, 5.0))
ax.text(6.7, 4.75, 'print("x:", 2.0, "m", sep=" | ", end="!\\n")', ha="center", fontsize=16, family=MONO, weight="bold")
parts = [("x:", 1.2, L_BLUE, "value 1"), (" | ", 1.2, L_ORANGE, "sep"), ("2.0", 1.2, L_BLUE, "value 2"), (" | ", 1.2, L_ORANGE, "sep"),
         ("m", 1.2, L_BLUE, "value 3"), ("!", 0.8, L_GREEN, "end"), ("\\n", 1.0, L_GREEN, "end")]
x = 2.0
for t, w, c, lab in parts:
    ax.add_patch(Rectangle((x, 2.5), w, 1.0, fc=c, ec=BLACK, lw=1.4))
    ax.text(x + w / 2, 3.0, t, ha="center", va="center", fontsize=15, family=MONO, weight="bold")
    ax.text(x + w / 2, 2.2, lab, ha="center", va="center", fontsize=11)
    x += w
ax.text(1.7, 3.0, "print builds:", ha="right", va="center", fontsize=12.5)
ax.text(1.7, 0.95, "you see:", ha="right", va="center", fontsize=12.5)
ax.add_patch(Rectangle((2.0, 0.5), 7.8, 0.9, fc=TERM_BG, ec=BLACK))
ax.text(2.2, 0.95, "x: | 2.0 | m!", va="center", fontsize=15, family=MONO, color=OUTC)
ax.text(10.1, 3.55, "sep goes BETWEEN values\n(normally one space)", fontsize=11.5, va="top", color=ORANGE, weight="bold")
ax.text(10.1, 2.6, "end goes AFTER the last\n(normally a newline)", fontsize=11.5, va="top", color=GREEN, weight="bold")
ax.set_xlim(0, 13.6); ax.set_ylim(0.3, 5.1); ax.axis("off")
save(fig, "fig01-how-print-builds-a-line.png")


# ---------- Figure 2: carriage return overwrites a line ----------
def term_row(ax, y, text, cursor, ghost=-1):
    for i in range(14):
        c = text[i] if i < len(text) else " "
        ax.add_patch(Rectangle((i * 0.62 + 2.6, y), 0.62, 0.8, fc=TERM_BG, ec="#555555", lw=0.8))
        col = RED if i == ghost else TERM_FG
        ax.text(i * 0.62 + 2.91, y + 0.4, c, ha="center", va="center", fontsize=14, family=MONO, color=col, weight="bold")
    ax.add_patch(Rectangle((cursor * 0.62 + 2.6, y), 0.62, 0.8, fc="none", ec=ORANGE, lw=3))


fig, ax = plt.subplots(figsize=(13.5, 5.2))
rows = [('print("battery 100%", end="")', "battery 100%", 12, -1, ""),
        (r'print("\r", end="")', "battery 100%", 0, -1, "the cursor (orange) jumps back to the start"),
        ('print("battery 99%", end="")', "battery 99%%", 11, 11, "new text covers the old, but the last % is left over")]
for i, (code, text, cur, ghost, note) in enumerate(rows):
    y = 3.4 - i * 1.5
    ax.text(0.1, y + 1.02, code, fontsize=12, family=MONO, weight="bold")
    term_row(ax, y, text, cur, ghost)
    ax.text(11.5, y + 0.4, note, fontsize=11, va="center", wrap=True)
ax.set_xlim(0, 17.5); ax.set_ylim(0.2, 4.8); ax.axis("off")
save(fig, "fig02-carriage-return.png")

# ---------- Figure 3: input pauses the program ----------
fig, ax = plt.subplots(figsize=(13.5, 6.0))
ax.text(0.2, 4.55, "PROGRAM", fontsize=13, weight="bold", color=BLUE, va="center")
ax.text(0.2, 2.15, "PERSON", fontsize=13, weight="bold", color=ORANGE, va="center")
ax.plot([1.9, 13.3], [3.3, 3.3], color=L_GREY, lw=1.5, ls="--")
rbox(ax, 1.9, 4.0, 2.7, 1.1, "shows the prompt\nHow far (m)?", L_BLUE, 11.5)
ax.add_patch(Rectangle((5.0, 4.25), 3.7, 0.6, fc="white", ec=RED, lw=1.8, ls="--"))
ax.text(6.85, 4.55, "PAUSED: waiting ...", ha="center", va="center", fontsize=12, color=RED, weight="bold")
rbox(ax, 9.1, 4.0, 3.9, 1.1, "input gives back the TEXT\n'900'", L_GREEN, 11.5, MONO)
rbox(ax, 5.0, 1.6, 3.7, 1.1, "types 9 0 0\nthen presses Enter", L_ORANGE, 11.5)
arrow(ax, (3.3, 3.98), (5.6, 2.74), BLUE, 2.2)
arrow(ax, (8.1, 2.74), (10.4, 3.98), ORANGE, 2.2)
ax.text(3.3, 3.0, "the person reads it", fontsize=11, color=BLUE, ha="center")
ax.text(10.4, 3.0, "Enter sends the line", fontsize=11, color=ORANGE, ha="center")
ax.text(7.0, 0.8, 'route_m = float(input("How far (m)? "))', ha="center", fontsize=15, family=MONO, weight="bold")
ax.text(7.0, 0.25, "input always gives text. float turns it into a number.", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0, 13.4); ax.set_ylim(0, 5.3); ax.axis("off")
save(fig, "fig03-input-pauses-the-program.png")

# ---------- Figure 4: input, process, output ----------
fig, ax = plt.subplots(figsize=(13.5, 5.2))
heads = [("INPUT", "bring values in", L_ORANGE), ("PROCESS", "calculate", L_BLUE), ("OUTPUT", "show the answer", L_GREEN)]
for i, (t, sub, c) in enumerate(heads):
    rbox(ax, 2.6 + i * 3.8, 3.3, 3.0, 1.3, t + "\n" + sub, c, 13, weight="bold")
    if i < 2:
        arrow(ax, (5.65 + i * 3.8, 3.95), (6.35 + i * 3.8, 3.95), BLACK, 2.5)
rows = [("this program", ["type route and speed", "time = route / speed", "print minutes, seconds"]),
        ("a robot's loop", ["SENSE: read sensors", "THINK: compute a command", "ACT: drive the motors"]),
        ("a GPS line", ["line of text", "split, slice, float", "latitude, longitude"])]
for r, (name, cols) in enumerate(rows):
    y = 2.45 - r * 0.95
    ax.text(2.3, y, name, ha="right", va="center", fontsize=12, weight="bold")
    for i, t in enumerate(cols):
        ax.text(4.1 + i * 3.8, y, t, ha="center", va="center", fontsize=11.5)
ax.set_xlim(0, 13.6); ax.set_ylim(0.2, 4.9); ax.axis("off")
save(fig, "fig04-input-process-output.png")

# ---------- Figure 5: wheel calibration ----------
fig, ax = plt.subplots(figsize=(13.5, 5.0))
ax.plot([0, 1.1], [0, 0], color=BLACK, lw=2)
for k in range(0, 12):
    v = k * 0.1
    ax.plot([v, v], [0, -0.05], color=BLACK, lw=1.5)
    ax.text(v, -0.13, f"{v:.1f}", ha="center", fontsize=10.5, family=MONO)
ax.text(0.55, -0.26, "the tape on the floor (metres)", ha="center", fontsize=12)
for x, col, lab, yy in [(0.998, BLUE, "Rover believes: 0.998 m", 0.34), (1.012, RED, "the tape says: 1.012 m", 0.48)]:
    ax.plot([0, x], [yy - 0.14, yy - 0.14], color=col, lw=0)
    ax.plot([x, x], [0, yy - 0.04], color=col, lw=2.5)
    ax.text(x + 0.005, yy, lab, ha="right", fontsize=12.5, color=col, weight="bold", family=MONO)
ax.add_patch(Rectangle((0.0, 0.03), 0.08, 0.1, fc=ORANGE, ec=BLACK))
ax.text(0.04, 0.17, "start", ha="center", fontsize=11)
ax.text(0.45, 0.1, "the same 2640 encoder ticks", ha="center", fontsize=12, color=GREY, style="italic")
ax.text(0.55, 0.68, "If the wheel rolled further than Rover believes, the wheel is bigger than the data sheet says",
        ha="center", fontsize=13, weight="bold")
ax.text(0.55, -0.4, "true diameter = tape distance / (turns x pi) = 1.012 / (4.889 x 3.14159) = 0.06589 m", ha="center",
        fontsize=13, family=MONO)
ax.set_xlim(-0.05, 1.15); ax.set_ylim(-0.48, 0.76); ax.axis("off")
save(fig, "fig05-wheel-calibration.png")

# ---------- Figure 6: a battery bar made of characters ----------
fig, ax = plt.subplots(figsize=(13.5, 4.0))
filled = 87 * 20 // 100
for i in range(20):
    ch = "#" if i < filled else "-"
    ax.add_patch(Rectangle((i * 0.5 + 0.8, 1.5), 0.5, 0.9, fc=L_GREEN if i < filled else L_GREY, ec=BLACK, lw=1))
    ax.text(i * 0.5 + 1.05, 1.95, ch, ha="center", va="center", fontsize=15, family=MONO, weight="bold")
ax.text(0.6, 1.95, "[", ha="center", va="center", fontsize=22, family=MONO, weight="bold")
ax.text(11.0, 1.95, "]  87%", ha="left", va="center", fontsize=20, family=MONO, weight="bold")
ax.plot([0.8, 0.8, 9.3, 9.3], [1.35, 1.2, 1.2, 1.35], color=GREEN, lw=2.5)
ax.plot([9.3, 9.3, 10.8, 10.8], [1.35, 1.2, 1.2, 1.35], color=GREY, lw=2.5)
ax.text(5.05, 0.85, '"#" * 17', ha="center", fontsize=14, family=MONO, color=GREEN, weight="bold")
ax.text(10.05, 0.85, '"-" * 3', ha="center", fontsize=14, family=MONO, color=GREY, weight="bold")
ax.text(6.5, 2.9, "filled = 87 * 20 // 100 = 1740 // 100 = 17 characters out of 20", ha="center", fontsize=14, family=MONO)
ax.set_xlim(0.2, 13.2); ax.set_ylim(0.6, 3.2); ax.axis("off")
save(fig, "fig06-battery-bar.png")
print("figures saved in", os.path.abspath(OUT))
