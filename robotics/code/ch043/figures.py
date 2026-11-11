# Figures for Chapter 43 - Straight lines: slope and y = mx + c.
# Run:  python figures.py      (saves PNG files in ../../images/ch043/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch043")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def plane(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.grid(alpha=0.35)
    ax.axhline(0, color=BLACK, lw=1.3); ax.axvline(0, color=BLACK, lw=1.3)


# Figure 1: rise over run
fig, ax = plt.subplots(figsize=(8, 6.4))
plane(ax, (-1, 7), (-1, 5.5))
x = np.linspace(-1, 7, 10)
ax.plot(x, 0.75 * x + 0.25, color=BLUE, lw=3, label="y = 0.75x + 0.25")
ax.plot([1, 5], [1, 1], color=GREEN, lw=3); ax.plot([5, 5], [1, 4], color=RED, lw=3)
ax.text(3, 0.6, "run = 5 - 1 = 4", ha="center", fontsize=13, color=GREEN)
ax.text(5.15, 2.5, "rise = 4 - 1 = 3", fontsize=13, color=RED, va="center")
for px, py, lab in [(1, 1, "p (1, 1)"), (5, 4, "q (5, 4)")]:
    ax.plot([px], [py], "o", color=ORANGE, mec=BLACK, ms=12, zorder=5)
    ax.text(px - 0.3, py + 0.3, lab, fontsize=12.5, ha="right")
ax.plot([0], [0.25], "s", color=BLACK, ms=8, zorder=5); ax.text(0.15, -0.55, "c = 0.25: where the line crosses the y axis", fontsize=11.5)
ax.text(1.0, 4.6, "slope m = rise / run = 3 / 4 = 0.75", fontsize=13.5, weight="bold")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.74))
save(fig, "fig01-rise-over-run.png")

# Figure 2: four kinds of slope
fig, axes = plt.subplots(1, 4, figsize=(14, 3.9))
x = np.linspace(-2, 2, 10)
for ax, title in zip(axes, ["positive: goes up", "negative: goes down", "zero: flat", "vertical: no slope"]):
    plane(ax, (-2.5, 2.5), (-2.5, 2.5)); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, fontsize=13)
axes[0].plot(x, 0.8 * x, color=BLUE, lw=3); axes[1].plot(x, -0.8 * x + 0.5, color=BLUE, lw=3)
axes[2].plot(x, 0 * x + 1, color=BLUE, lw=3); axes[3].plot([1, 1], [-2.2, 2.2], color=BLUE, lw=3)
axes[0].text(-2.3, -2.3, "m = 0.8", fontsize=12); axes[1].text(-2.3, -2.3, "m = -0.8", fontsize=12)
axes[2].text(-2.3, -2.3, "m = 0, y = 1", fontsize=12); axes[3].text(-2.3, 1.9, "x = 1, run = 0", fontsize=12)
save(fig, "fig02-kinds-of-slope.png")

# Figure 3: a family of lines
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
x = np.linspace(-4, 4, 10)
styles = ["-", "--", ":", "-."]
for (m, col), st in zip([(0.5, GREEN), (1, BLUE), (2, RED), (-1, ORANGE)], styles):
    axes[0].plot(x, m * x, color=col, lw=2.8, ls=st, label=f"y = {m}x")
axes[0].set_title("same c = 0, different slope m", fontsize=13)
for (c, col), st in zip([(-2, GREEN), (0, BLUE), (1.5, RED)], styles):
    axes[1].plot(x, 0.5 * x + c, color=col, lw=2.8, ls=st, label=f"y = 0.5x + {c}")
axes[1].set_title("same m = 0.5, different c: parallel lines", fontsize=13)
for ax in axes:
    plane(ax, (-4, 4), (-4, 4)); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig03-family.png")

# Figure 4: mapping one range onto another
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
r = np.array([0, 1023])
axes[0].plot(r, r * 5 / 1023, color=BLUE, lw=3)
axes[0].plot([512], [512 * 5 / 1023], "o", color=ORANGE, mec=BLACK, ms=11)
axes[0].annotate("512 -> 2.502 V", (512, 2.502), xytext=(560, 1.2), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
axes[0].set_xlabel("ADC reading (counts)"); axes[0].set_ylabel("voltage (V)"); axes[0].set_title("ADC to volts", fontsize=13)
axes[1].plot(r, -100 + r * 200 / 1023, color=GREEN, lw=3)
axes[1].axhline(0, color=BLACK, lw=1)
axes[1].plot([256], [-100 + 256 * 200 / 1023], "o", color=ORANGE, mec=BLACK, ms=11)
axes[1].annotate("256 -> -50 %", (256, -49.95), xytext=(330, -80), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
axes[1].set_xlabel("joystick reading (counts)"); axes[1].set_ylabel("speed command (%)"); axes[1].set_title("joystick to speed", fontsize=13)
for ax in axes:
    ax.grid(alpha=0.3); ax.set_xlim(0, 1023)
save(fig, "fig04-linear-map.png")

# Figure 5: load cell calibration
m = 2.0 / (52713 - 8421); c = -m * 8421
raw = np.linspace(0, 65000, 10)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(raw, m * raw + c, color=BLUE, lw=3, label="calibration line: mass = m x raw + c")
ax.plot([8421, 52713], [0, 2], "o", color=BLACK, ms=11, label="the two calibration points")
ax.plot([61000], [m * 61000 + c], "s", color=ORANGE, mec=BLACK, ms=11, label="an unknown load: 2.374 kg")
ax.axhline(0, color=BLACK, lw=1)
ax.annotate("empty scale: 8421 counts", (8421, 0), xytext=(14000, -0.55), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("raw reading from the load cell (counts)"); ax.set_ylabel("mass (kg)"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
ax.set_xlim(0, 65000); ax.set_ylim(-0.8, 3)
save(fig, "fig05-load-cell.png")

# Figure 6: lane lines in a camera image
fig, ax = plt.subplots(figsize=(9, 7))
ax.add_patch(Rectangle((0, 0), 640, 480, fc=L_GREY, ec=BLACK))
ax.add_patch(Polygon([(83.6, 479), (224.1, 280), (414.7, 280), (566.9, 479)], closed=True, fc="#C8C8C8", ec="none"))
for (p, q) in [((210, 300), (90, 470)), ((430, 300), (560, 470))]:
    a = (q[0] - p[0]) / (q[1] - p[1]); b = p[0] - a * p[1]
    rows = np.array([260, 479])
    ax.plot(a * rows + b, rows, color=BLUE, lw=3)
    ax.plot([p[0], q[0]], [p[1], q[1]], "o", color=BLACK, ms=9, zorder=5)
ax.plot([325.3, 325.3], [380, 479], color=GREEN, lw=3, label="lane centre, x = 325.3")
ax.plot([320, 320], [380, 479], color=ORANGE, lw=3, ls="--", label="camera centre, x = 320")
ax.text(20, 30, "pixel (0, 0) is the TOP left corner; rows grow downward", fontsize=12)
ax.text(10, 465, "x = 83.6", fontsize=11.5, color=BLUE); ax.text(575, 465, "x = 566.9", fontsize=11.5, color=BLUE)
ax.set_xlim(-5, 690); ax.set_ylim(485, -5); ax.set_aspect("equal"); ax.set_xlabel("column (pixels)"); ax.set_ylabel("row (pixels)")
ax.legend(loc="center left", fontsize=11)
save(fig, "fig06-lane-lines.png")
print("figures saved in", os.path.abspath(OUT))
