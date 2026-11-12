# Figures for Chapter 97 - C++ for Arduino part 2: if, loops, functions, arrays.
# Run:  python figures.py      (saves PNG files in ../../images/ch097/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch097")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=11, weight="normal", family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, family=family)


def diamond(ax, x, y, w, h, text, fs=10.5):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y + h), (x + w, y + h / 2), (x + w / 2, y)], fc=L_BLUE, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, family="monospace")


def arrow(ax, x1, y1, x2, y2, color=BLACK, lw=1.8, text=None, tx=0, ty=0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=15, color=color, lw=lw))
    if text:
        ax.text((x1 + x2) / 2 + tx, (y1 + y2) / 2 + ty, text, fontsize=10.5, color=color)


# Figure 1: the if / else if / else chain of decide()
fig, ax = plt.subplots(figsize=(11, 6.4))
qs = [("bump", "BACK_UP", L_RED), ("cm < 20", "TURN", L_ORANGE), ("cm < 50", "SLOW", L_ORANGE)]
for k, (q, act, col) in enumerate(qs):
    y = 5.0 - k * 1.8
    diamond(ax, 0.5, y, 3.0, 1.2, q)
    box(ax, 5.2, y + 0.2, 2.6, 0.8, f"return {act}", col, family="monospace")
    arrow(ax, 3.55, y + 0.6, 5.15, y + 0.6, color=GREEN, text="true", tx=-0.3, ty=0.12)
    if k < 2:
        arrow(ax, 2.0, y - 0.05, 2.0, y - 0.55, color=RED, text="false", tx=0.15, ty=0.0)
arrow(ax, 2.0, 1.35, 2.0, 0.85, color=RED, text="false", tx=0.15)
box(ax, 0.7, 0.05, 2.6, 0.8, "return GO", L_GREEN, family="monospace")
arrow(ax, 2.0, 6.75, 2.0, 6.25)
ax.text(2.0, 6.85, "decide(cm, bump)", ha="center", fontsize=12, family="monospace")
ax.text(8.3, 5.6, "1. the most important rule\n   is asked first", fontsize=11)
ax.text(8.3, 3.8, "2. only ONE branch runs:\n   the first true one", fontsize=11)
ax.text(8.3, 2.0, "3. if every test is false,\n   the last line runs", fontsize=11)
ax.set_xlim(0, 11.5); ax.set_ylim(-0.1, 7.2); ax.axis("off")
save(fig, "fig01-if-chain.png")

# Figure 2: the decisions over all distances, bumper free and pressed
fig, ax = plt.subplots(figsize=(11, 3.6))
for row, bump in [(1, False), (0, True)]:
    if bump:
        ax.add_patch(Rectangle((0, row), 200, 0.8, fc=L_RED, ec=BLACK))
        ax.text(100, row + 0.4, "BACK UP (whatever the distance)", ha="center", va="center", fontsize=11)
    else:
        for a, b, name, col in [(0, 20, "TURN", L_ORANGE), (20, 50, "SLOW", L_GREY), (50, 200, "GO", L_GREEN)]:
            ax.add_patch(Rectangle((a, row), b - a, 0.8, fc=col, ec=BLACK))
            ax.text((a + b) / 2, row + 0.4, name, ha="center", va="center", fontsize=11)
ax.set_yticks([0.4, 1.4]); ax.set_yticklabels(["bumper\npressed", "bumper\nfree"])
ax.set_xlim(0, 200); ax.set_ylim(-0.1, 1.9); ax.set_xlabel("distance to the nearest obstacle (cm)")
for x in (20, 50):
    ax.axvline(x, color=BLACK, ls="--", lw=1)
save(fig, "fig02-decision-map.png")

# Figure 3: switch with and without break
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, title, has_break in [(axes[0], "with break: only one case runs", True), (axes[1], "break forgotten: falls through", False)]:
    cases = ["case GO:", "case SLOW:", "case TURN:", "default:"]
    for k, c in enumerate(cases):
        y = 3.6 - k * 1.1
        col = L_GREEN if (k == 1 or (not has_break and k > 1)) else L_GREY
        box(ax, 0.3, y, 2.4, 0.8, c, col, family="monospace")
        ax.text(3.0, y + 0.4, "print ..." + ("; break;" if has_break and k < 3 else ";"), fontsize=10.5, family="monospace", va="center")
    ax.annotate("action\nis SLOW", xy=(0.25, 2.9), xytext=(-1.0, 2.9), fontsize=11, va="center", ha="center",
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
    if has_break:
        arrow(ax, 6.0, 2.9, 6.0, -0.2, color=BLUE)
        ax.text(6.15, 1.3, "jump out", fontsize=10.5, color=BLUE)
    else:
        for y in (2.9, 1.8):
            arrow(ax, 2.0, y - 0.1, 2.0, y - 0.4, color=RED)
        ax.text(3.0, -0.6, "SLOW, TURN and the default all run!", fontsize=11, color=RED)
    ax.set_title(title, fontsize=12)
    ax.set_xlim(-1.8, 7.5); ax.set_ylim(-0.9, 4.6); ax.axis("off")
save(fig, "fig03-switch-break.png")

# Figure 4: the three parts of a for loop
fig, ax = plt.subplots(figsize=(11, 5))
ax.text(5.5, 4.6, "for (int i = 0;   i < N;   i++) {  ...  }", ha="center", fontsize=15, family="monospace")
for x_code, x, t, col in [(3.95, 2.6, "1. start (once)", GREEN), (5.6, 5.6, "2. test (before each pass)", BLUE),
                          (6.85, 8.8, "3. step (after each pass)", ORANGE)]:
    ax.annotate(t, xy=(x_code, 4.4), xytext=(x, 3.5), ha="center", fontsize=11, color=col,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.5))
box(ax, 0.4, 1.6, 2.0, 0.9, "i = 0", L_GREEN, family="monospace")
diamond(ax, 3.2, 1.45, 2.4, 1.2, "i < N ?")
box(ax, 6.6, 1.6, 2.0, 0.9, "the body", L_GREY)
box(ax, 6.6, 0.0, 2.0, 0.8, "i++", L_ORANGE, family="monospace")
box(ax, 3.4, -0.5, 2.0, 0.7, "after the loop", L_BLUE)
arrow(ax, 2.45, 2.05, 3.15, 2.05)
arrow(ax, 5.65, 2.05, 6.55, 2.05, color=GREEN, text="true", tx=-0.25, ty=0.15)
arrow(ax, 7.6, 1.55, 7.6, 0.85)
ax.annotate("", xy=(4.4, 1.4), xytext=(6.55, 0.4), arrowprops=dict(arrowstyle="-|>", lw=1.8, connectionstyle="arc3,rad=-0.3"))
arrow(ax, 4.4, 1.4, 4.4, 0.25, color=RED, text="false", tx=0.1)
ax.set_xlim(0, 11); ax.set_ylim(-0.7, 5.0); ax.axis("off")
save(fig, "fig04-for-loop.png")

# Figure 5: SRAM: globals at the bottom, the stack growing down from the top
fig, ax = plt.subplots(figsize=(10, 6.6))
ax.add_patch(Rectangle((2, 0), 3, 10, fc="white", ec=BLACK, lw=2))
ax.add_patch(Rectangle((2, 0), 3, 2.0, fc=L_BLUE, ec=BLACK)); ax.text(3.5, 1.0, "global variables\n(and static ones)", ha="center", va="center", fontsize=10.5)
ax.add_patch(Rectangle((2, 2.0), 3, 0.8, fc=L_GREY, ec=BLACK)); ax.text(3.5, 2.4, "Serial buffers", ha="center", va="center", fontsize=10.5)
frames = [("loop(): raw, smoothed", L_ORANGE), ("smooth(): newReading", L_GREEN), ("analogRead(): its own locals", L_RED)]
for k, (t, col) in enumerate(frames):
    y = 10 - (k + 1) * 1.1
    ax.add_patch(Rectangle((2, y), 3, 1.1, fc=col, ec=BLACK)); ax.text(3.5, y + 0.55, t, ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((2, 2.8), 3, 3.9, fc="#F7F7F7", ec=BLACK, hatch="..")); ax.text(3.5, 4.75, "free", ha="center", va="center", fontsize=12)
ax.annotate("", xy=(5.6, 6.0), xytext=(5.6, 9.6), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
ax.text(5.8, 7.8, "the stack grows DOWN\nwith each function call,\nand shrinks when it returns", fontsize=11, color=RED, va="center")
ax.annotate("", xy=(5.6, 2.9), xytext=(5.6, 1.0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5))
ax.text(5.8, 1.9, "globals are fixed in size\n(the IDE's memory report)", fontsize=11, color=BLUE, va="center")
ax.text(1.8, 9.9, "address 2047", ha="right", fontsize=10); ax.text(1.8, 0.05, "address 0", ha="right", fontsize=10)
ax.text(3.5, 10.4, "the Uno's 2,048 bytes of SRAM", ha="center", fontsize=12)
ax.text(5.8, 4.7, "if the two meet, the stack writes\nover your variables: a crash", fontsize=11, va="center")
ax.set_xlim(0, 10.5); ax.set_ylim(-0.3, 10.8); ax.axis("off")
save(fig, "fig06-stack.png")

# Figure 6: an array in memory, and writing past its end
vals = [512, 518, 509, 530, 497, 515, 521, 508, 940, 513]
fig, ax = plt.subplots(figsize=(13, 3.6))
for i, v in enumerate(vals):
    ax.add_patch(Rectangle((i * 1.1, 1.0), 1.0, 1.0, fc=L_BLUE, ec=BLACK))
    ax.text(i * 1.1 + 0.5, 1.5, str(v), ha="center", va="center", fontsize=11)
    ax.text(i * 1.1 + 0.5, 2.25, f"[{i}]", ha="center", fontsize=10.5, family="monospace")
ax.add_patch(Rectangle((11.0, 1.0), 1.0, 1.0, fc=L_RED, ec=BLACK, hatch="//"))
ax.text(11.5, 2.25, "[10]", ha="center", fontsize=10.5, family="monospace", color=RED)
ax.text(11.5, 0.6, "NOT the array:\nthe next variable\nin memory", ha="center", va="top", fontsize=10, color=RED)
ax.text(5.0, 0.6, "int readings[10]: 10 ints x 2 bytes = 20 bytes, numbered 0 to 9", ha="center", va="top", fontsize=11)
ax.set_xlim(-0.3, 12.6); ax.set_ylim(-0.4, 2.7); ax.axis("off")
save(fig, "fig05-array.png")

# Figure 7: the moving average's ring of 8 readings
fig, ax = plt.subplots(figsize=(11, 3.8))
hist = [409, 402, 416, 395, 411, 388, 420, 407]
for i, v in enumerate(hist):
    col = L_RED if i == 3 else L_GREEN
    ax.add_patch(Rectangle((i * 1.2, 1.0), 1.1, 1.0, fc=col, ec=BLACK))
    ax.text(i * 1.2 + 0.55, 1.5, str(v), ha="center", va="center", fontsize=11)
    ax.text(i * 1.2 + 0.55, 2.25, f"[{i}]", ha="center", fontsize=10.5, family="monospace")
ax.annotate("next = 3: the OLDEST reading,\nreplaced by the new one", xy=(3 * 1.2 + 0.55, 0.95), xytext=(3 * 1.2 + 0.55, -0.2),
            ha="center", va="top", fontsize=10.5, color=RED, arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
ax.annotate("", xy=(0.4, 2.55), xytext=(9.2, 2.55), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.5, connectionstyle="arc3,rad=0.25"))
ax.text(4.8, 3.35, "after [7], next goes back to [0]:  next = (next + 1) % 8", ha="center", fontsize=11, color=GREY)
ax.text(10.0, 1.5, "sum = sum - old + new\naverage = sum / 8", fontsize=11, va="center")
ax.set_xlim(-0.3, 13.5); ax.set_ylim(-1.3, 3.7); ax.axis("off")
save(fig, "fig07-ring.png")

# Figure 8: raw and smoothed readings for three window sizes (PC test bench outputs)
fig, axes = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
for ax, w in zip(axes, [4, 8, 16]):
    rows = [tuple(map(int, l.split())) for l in open(os.path.join(HERE, "pc_tests", f"step_window{w}.txt"))]
    t = [k * 0.1 for k in range(len(rows))]
    ax.plot(t, [r for r, s in rows], color=GREY, lw=1.2, marker=".", label="raw readings")
    ax.plot(t, [s for r, s in rows], color=BLUE, lw=2.5, label=f"average of the last {w}")
    ax.axhline(409, color=BLACK, ls="--", lw=1); ax.axhline(614, color=BLACK, ls="--", lw=1)
    ax.axvline(2.0, color=RED, ls=":", lw=1.5)
    ax.set_ylabel("ADC count"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10)
    ax.set_ylim(330, 690)
axes[0].text(2.05, 345, "the sensor jumps from 2.0 V to 3.0 V", color=RED, fontsize=10.5)
axes[2].set_xlabel("time (s)")
fig.tight_layout()
save(fig, "fig08-smoothing.png")
print("figures saved in", os.path.abspath(OUT))
