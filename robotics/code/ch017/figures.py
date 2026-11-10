# Figures for Chapter 17 — True and false: booleans and comparisons.
# Run:  python figures.py      (saves PNG files in ../../images/ch017/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Wedge, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch017")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=GREY, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw))


def rbox(ax, x, y, w, h, text, face, size=12, family=None, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


# ---------- Figure 1: a comparison splits the number line ----------
fig, axes = plt.subplots(2, 1, figsize=(13, 5.8))
for ax, code, closed in [(axes[0], "distance_m > 0.30", False), (axes[1], "distance_m >= 0.30", True)]:
    ax.add_patch(Rectangle((0, -0.09), 0.3, 0.18, fc=L_RED, ec="none"))
    ax.add_patch(Rectangle((0.3, -0.09), 0.7, 0.18, fc=L_GREEN, ec="none"))
    ax.plot([0, 1], [0, 0], color=BLACK, lw=1.5)
    for v in (0.0, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0):
        ax.plot([v, v], [-0.13, -0.09], color=BLACK, lw=1.5)
        ax.text(v, -0.27, f"{v:.2f}", ha="center", fontsize=11, family=MONO)
    ax.plot(0.3, 0, "o", ms=15, mfc=GREEN if closed else "white", mec=BLACK, mew=2, zorder=5)
    ax.text(0.15, 0.17, "False", ha="center", fontsize=14, color=RED, weight="bold")
    ax.text(0.65, 0.17, "True", ha="center", fontsize=14, color=GREEN, weight="bold")
    ax.text(-0.02, 0, code, ha="right", va="center", fontsize=13, family=MONO, weight="bold")
    note = "exactly 0.30 counts as True (filled circle)" if closed else "exactly 0.30 counts as False (empty circle)"
    ax.text(0.32, -0.46, note, ha="left", fontsize=12, style="italic")
    ax.set_xlim(-0.5, 1.03); ax.set_ylim(-0.55, 0.3); ax.axis("off")
save(fig, "fig01-comparison-on-a-line.png")

# ---------- Figure 2: = stores, == asks ----------
fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))
ax = axes[0]
ax.text(3.0, 4.3, "speed = 0.5", ha="center", fontsize=18, family=MONO, weight="bold")
ax.text(3.0, 3.75, "an ORDER: store this value", ha="center", fontsize=13, color=BLUE, weight="bold")
ax.add_patch(Rectangle((1.9, 1.3), 2.2, 1.2, fc=L_BLUE, ec=BLACK, lw=1.5))
ax.text(3.0, 1.95, "0.5", ha="center", va="center", fontsize=16, family=MONO, weight="bold")
ax.add_patch(FancyBboxPatch((2.1, 0.92), 1.8, 0.42, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=BLACK))
ax.text(3.0, 1.13, "speed", ha="center", va="center", fontsize=12, family=MONO)
arrow(ax, (3.0, 3.5), (3.0, 2.55), BLUE, 2.5)
ax.text(3.0, 0.4, "the box changes; nothing is answered", ha="center", fontsize=12, style="italic")
ax.set_xlim(0, 6); ax.set_ylim(0.1, 4.7); ax.axis("off")
ax = axes[1]
ax.text(3.0, 4.3, "speed == 0.5", ha="center", fontsize=18, family=MONO, weight="bold")
ax.text(3.0, 3.75, "a QUESTION: are these equal?", ha="center", fontsize=13, color=GREEN, weight="bold")
ax.add_patch(Rectangle((0.7, 1.3), 1.8, 1.2, fc=L_BLUE, ec=BLACK, lw=1.5))
ax.text(1.6, 1.95, "0.5", ha="center", va="center", fontsize=16, family=MONO, weight="bold")
ax.add_patch(FancyBboxPatch((0.85, 0.92), 1.5, 0.42, boxstyle="round,pad=0.02,rounding_size=0.08", fc="white", ec=BLACK))
ax.text(1.6, 1.13, "speed", ha="center", va="center", fontsize=12, family=MONO)
ax.text(2.95, 1.95, "?", ha="center", va="center", fontsize=26, weight="bold", color=GREEN)
ax.text(3.75, 1.95, "0.5", ha="center", va="center", fontsize=16, family=MONO, weight="bold")
arrow(ax, (4.3, 1.95), (4.9, 1.95), GREEN, 2.5)
ax.text(5.5, 1.95, "True", ha="center", va="center", fontsize=16, family=MONO, weight="bold", color=GREEN)
ax.text(3.0, 0.4, "the box stays the same; you get an answer", ha="center", fontsize=12, style="italic")
ax.set_xlim(0, 6.2); ax.set_ylim(0.1, 4.7); ax.axis("off")
save(fig, "fig02-store-or-ask.png")


# ---------- Figure 3: truth tables ----------
def table(ax, x0, title, heads, rows, widths):
    ax.text(x0 + sum(widths) / 2, 5.55, title, ha="center", fontsize=15, weight="bold", family=MONO)
    x = x0
    for h, w in zip(heads, widths):
        ax.add_patch(Rectangle((x, 4.6), w, 0.7, fc=L_GREY, ec=BLACK))
        ax.text(x + w / 2, 4.95, h, ha="center", va="center", fontsize=12, weight="bold", family=MONO)
        x += w
    for r, row in enumerate(rows):
        x = x0
        y = 3.85 - r * 0.75
        for c, (v, w) in enumerate(zip(row, widths)):
            last = c == len(row) - 1
            face = "white" if not last else (L_GREEN if v else L_RED)
            ax.add_patch(Rectangle((x, y), w, 0.75, fc=face, ec=BLACK))
            ax.text(x + w / 2, y + 0.37, str(v), ha="center", va="center", fontsize=12.5, family=MONO, weight="bold" if last else "normal")
            x += w


fig, ax = plt.subplots(figsize=(14, 5.6))
T, F = True, False
table(ax, 0.2, "and", ["a", "b", "a and b"], [(T, T, T), (T, F, F), (F, T, F), (F, F, F)], [1.25, 1.25, 1.6])
table(ax, 5.1, "or", ["a", "b", "a or b"], [(T, T, T), (T, F, T), (F, T, T), (F, F, F)], [1.25, 1.25, 1.6])
table(ax, 10.0, "not", ["a", "not a"], [(T, F), (F, T)], [1.25, 1.6])
ax.text(2.25, 1.15, "True only if BOTH are True", ha="center", fontsize=12.5, color=BLUE, weight="bold")
ax.text(7.15, 1.15, "True if AT LEAST ONE is True", ha="center", fontsize=12.5, color=BLUE, weight="bold")
ax.text(11.42, 2.2, "swaps the answer", ha="center", fontsize=12.5, color=BLUE, weight="bold")
ax.set_xlim(0, 13.2); ax.set_ylim(0.9, 6.0); ax.axis("off")
save(fig, "fig03-truth-tables.png")


# ---------- Figure 4: and = series, or = parallel ----------
def switch(ax, x, y, label, closed):
    ax.plot(x, y, "o", color=BLACK, ms=7)
    ax.plot(x + 1.1, y, "o", color=BLACK, ms=7)
    if closed:
        ax.plot([x, x + 1.1], [y, y], color=GREEN, lw=3)
    else:
        ax.plot([x, x + 0.95], [y, y + 0.45], color=RED, lw=3)
    ax.text(x + 0.55, y + 0.58, label, ha="center", fontsize=11)


fig, axes = plt.subplots(2, 1, figsize=(13, 7.0))
ax = axes[0]
ax.text(5.8, 2.3, "AND: switches in a row. One open switch stops everything.", ha="center", fontsize=13.5, weight="bold")
xs = [1.6, 4.0, 6.4]
ax.plot([0.9, 1.6], [0.8, 0.8], color=BLACK, lw=2)
ax.plot([2.7, 4.0], [0.8, 0.8], color=BLACK, lw=2)
ax.plot([5.1, 6.4], [0.8, 0.8], color=BLACK, lw=2)
ax.plot([7.5, 8.9], [0.8, 0.8], color=BLACK, lw=2)
switch(ax, xs[0], 0.8, "battery_ok", True)
switch(ax, xs[1], 0.8, "bumper_clear", False)
switch(ax, xs[2], 0.8, "e_stop_clear", True)
rbox(ax, 0.0, 0.45, 0.9, 0.7, "power", L_ORANGE, 11)
rbox(ax, 8.9, 0.45, 1.3, 0.7, "motor", L_RED, 11, weight="bold")
ax.text(10.4, 0.8, "False: motor off", va="center", fontsize=12.5, color=RED, weight="bold")
ax.set_xlim(-0.1, 12.6); ax.set_ylim(0.2, 2.6); ax.axis("off")
ax = axes[1]
ax.text(5.8, 3.85, "OR: switches side by side. One closed switch is enough.", ha="center", fontsize=13.5, weight="bold")
ax.plot([0.9, 2.5], [1.55, 1.55], color=BLACK, lw=2)
ax.plot([2.5, 2.5], [0.6, 2.5], color=BLACK, lw=2)
ax.plot([6.0, 6.0], [0.6, 2.5], color=BLACK, lw=2)
ax.plot([6.0, 8.9], [1.55, 1.55], color=BLACK, lw=2)
for y, lab, closed in [(2.5, "phone_alarm", False), (0.6, "button_pressed", True)]:
    ax.plot([2.5, 3.7], [y, y], color=BLACK, lw=2)
    switch(ax, 3.7, y, lab, closed)
    ax.plot([4.8, 6.0], [y, y], color=BLACK, lw=2)
rbox(ax, 0.0, 1.2, 0.9, 0.7, "power", L_ORANGE, 11)
rbox(ax, 8.9, 1.2, 1.3, 0.7, "buzzer", L_GREEN, 11, weight="bold")
ax.text(10.4, 1.55, "True: buzzer on", va="center", fontsize=12.5, color=GREEN, weight="bold")
ax.set_xlim(-0.1, 12.6); ax.set_ylim(0.2, 4.1); ax.axis("off")
save(fig, "fig04-and-or-as-switches.png")

# ---------- Figure 5: a tolerance band ----------
fig, ax = plt.subplots(figsize=(13, 4.8))
ax.axhspan(0.28, 0.32, color=L_GREEN, label="tolerance band: 0.30 +/- 0.02")
ax.axhline(0.30, color=BLACK, ls="--", lw=2, label="setpoint 0.30 m")
t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
v = [0.45, 0.38, 0.335, 0.312, 0.3004, 0.2951, 0.2988, 0.3032, 0.2997, 0.3011]
ax.plot(t, v, "-o", color=BLUE, lw=2, label="measured distance")
ax.annotate("first reading inside the band:\nabs(x - 0.30) <= 0.02 is True", xy=(3, 0.312), xytext=(3.7, 0.41), fontsize=12,
            arrowprops=dict(arrowstyle="-|>", color=BLACK))
ax.annotate("never exactly 0.30, so x == 0.30 stays False", xy=(6, 0.2988), xytext=(4.4, 0.245), fontsize=12,
            arrowprops=dict(arrowstyle="-|>", color=BLACK))
ax.set_xlabel("loop number"); ax.set_ylabel("distance (m)")
ax.set_xlim(-0.2, 9.3); ax.set_ylim(0.23, 0.47)
ax.grid(alpha=0.3); ax.legend(loc="upper right", framealpha=1)
save(fig, "fig05-tolerance-band.png")

# ---------- Figure 6: the short way round a compass ----------
fig, ax = plt.subplots(figsize=(10.5, 8.5))
ax.add_patch(Circle((0, 0), 1.0, fc="white", ec=BLACK, lw=2))
for d in range(0, 360, 30):
    a = math.radians(90 - d)
    ax.plot([0.93 * math.cos(a), math.cos(a)], [0.93 * math.sin(a), math.sin(a)], color=BLACK, lw=1.5)
    ax.text(1.12 * math.cos(a), 1.12 * math.sin(a), str(d), ha="center", va="center", fontsize=11)
ax.add_patch(Wedge((0, 0), 0.5, 105, 450, width=0.05, fc=L_RED, ec=RED))
for d, col in [(0, BLACK), (345, BLUE)]:
    a = math.radians(90 - d)
    ax.annotate("", xy=(0.9 * math.cos(a), 0.9 * math.sin(a)), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=3, ls="--" if d == 0 else "-"))
ax.add_patch(Wedge((0, 0), 0.72, 90, 90 + 15, width=0.07, fc=GREEN, ec=GREEN))
ax.annotate("short way: 1 degree", xy=(-0.1, 0.68), xytext=(-2.15, 1.25), fontsize=12.5, color=GREEN, weight="bold",
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.8))
ax.annotate("long way: 359 degrees\n(what abs(359 - 0) measures)", xy=(0.33, -0.36), xytext=(1.0, -1.42), fontsize=12.5,
            color=RED, weight="bold", ha="center", arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8))
ax.text(0.0, 1.5, "target 0 (black, dashed) and robot 359 (blue, drawn further apart so you can see it)", ha="center", fontsize=11.5)
ax.text(-0.75, -1.72, "(359 - 0 + 180) % 360 - 180  =  -1", ha="center", fontsize=13, family=MONO, weight="bold")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.85, 1.65); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-heading-error.png")
print("figures saved in", os.path.abspath(OUT))
