# Figures for Chapter 86 - Diodes and flyback protection.
# Run:  python figures.py      (saves PNG files in ../../images/ch086/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch086")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


def diode_sym(ax, x, y, horizontal=True, zener=False, color=BLACK, scale=1.0):
    s = 0.35 * scale
    if horizontal:
        ax.add_patch(plt.Polygon([(x - s, y - s), (x - s, y + s), (x + s, y)], color=color))
        line(ax, [x + s, x + s], [y - s, y + s], color=color, lw=3)
        if zener:
            line(ax, [x + s, x + s + 0.15], [y + s, y + s + 0.1], color=color, lw=3); line(ax, [x + s, x + s - 0.15], [y - s, y - s - 0.1], color=color, lw=3)
    else:   # pointing up
        ax.add_patch(plt.Polygon([(x - s, y - s), (x + s, y - s), (x, y + s)], color=color))
        line(ax, [x - s, x + s], [y + s, y + s], color=color, lw=3)


# Figure 1: the p-n junction and the symbol
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 8.5); ax.set_ylim(-2.0, 4.2)
ax.add_patch(plt.Rectangle((0, 0), 4, 3, color=L_ORANGE, ec=BLACK)); ax.add_patch(plt.Rectangle((4, 0), 4, 3, color=L_BLUE, ec=BLACK))
ax.text(2, 3.3, "p-type silicon\n(extra 'holes', +)", ha="center", fontsize=10.5); ax.text(6, 3.3, "n-type silicon\n(extra electrons, -)", ha="center", fontsize=10.5)
for x in np.linspace(0.5, 3.0, 5):
    for y in [0.6, 1.5, 2.4]:
        ax.text(x, y, "+", ha="center", va="center", color=RED, fontsize=12)
for x in np.linspace(5.0, 7.5, 5):
    for y in [0.6, 1.5, 2.4]:
        ax.text(x, y, "-", ha="center", va="center", color=BLUE, fontsize=14)
ax.add_patch(plt.Rectangle((3.4, 0), 1.2, 3, color="white", ec=GREY, ls="--"))
ax.text(4, -1.0, "the junction: an empty 'gate' that needs\nabout 0.6 V forwards to open", ha="center", fontsize=10.5)
ax.set_title("inside a diode", fontsize=11.5)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 7), ax.set_ylim(-1.5, 4.8)
line(ax, [0, 2.6], [2, 2]); diode_sym(ax, 3, 2, scale=1.4); line(ax, [3.5, 6], [2, 2])
ax.text(0.3, 2.4, "anode", fontsize=10.5); ax.text(4.6, 2.4, "cathode", fontsize=10.5)
ax.annotate("", xy=(5.5, 1.0), xytext=(0.5, 1.0), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=GREEN)); ax.text(3, 0.5, "current flows this way (forward)", ha="center", color=GREEN, fontsize=10.5)
ax.add_patch(plt.Rectangle((0.8, 3.0), 4.4, 0.6, color=GREY, ec=BLACK)); ax.add_patch(plt.Rectangle((4.4, 3.0), 0.35, 0.6, color="white", ec=BLACK))
ax.text(3, 3.85, "real part: the stripe marks the cathode", ha="center", fontsize=10.5)
ax.set_title("its symbol", fontsize=11.5)
save(fig, "fig01-diode.png")

# Figure 2: I-V curves of silicon, Schottky and Zener
fig, ax = plt.subplots(figsize=(10, 5))
v = np.linspace(-6.5, 1.0, 2000)
si = np.where(v > 0, np.exp((v - 0.85) / 0.05), 0)
sch = np.where(v > 0, np.exp((v - 0.45) / 0.05), 0)
zn = np.where(v > 0, np.exp((v - 0.85) / 0.05), np.where(-v > 4.7, -0.01 * np.exp((-v - 5.1) / 0.05), 0))
for y, col, lab, ls in [(si, BLUE, "silicon rectifier", "-"), (sch, GREEN, "Schottky", "--"), (zn, RED, "5.1 V Zener", ":")]:
    ax.plot(v, np.clip(y, -1.2, 1.2), color=col, lw=2.5, ls=ls, label=lab)
ax.axhline(0, color=BLACK, lw=1); ax.axvline(0, color=BLACK, lw=1)
ax.text(-0.15, 0.75, "forward:\nconducts", fontsize=10.5, ha="right"); ax.text(-3, 0.25, "reverse: blocks", fontsize=10.5, ha="center")
ax.text(-5.0, -0.7, "the Zener breaks down\non purpose at 5.1 V", fontsize=10.5, color=RED, ha="left")
ax.set_xlabel("voltage across the diode (V)"); ax.set_ylabel("current (A)"); ax.set_ylim(-1.25, 1.25); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("a one-way valve: forwards above about 0.5 V (0.2 V for Schottky), backwards nothing", fontsize=11)
save(fig, "fig02-iv.png")

# Figure 3: flyback circuit and the release with diode vs diode+Zener
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw=dict(width_ratios=[1, 1.4]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 5), ax.set_ylim(-1.0, 6.4)
line(ax, [0, 0], [6, 5.4]); ax.text(0, 6.1, "+24 V", ha="center", color=RED, fontsize=11)
line(ax, [0, 0], [5.4, 4.8]);
for k in range(5):
    ax.add_patch(matplotlib.patches.Arc((0, 4.6 - k * 0.4), 0.5, 0.4, theta1=-90, theta2=90, color=ORANGE, lw=2.5))
line(ax, [0, 0], [2.8, 2.2]); ax.text(-0.6, 3.8, "valve\ncoil", ha="right", fontsize=10.5)
line(ax, [0, 2.0], [5.2, 5.2]); line(ax, [0, 2.0], [2.4, 2.4]); line(ax, [2.0, 2.0], [2.4, 3.4]); diode_sym(ax, 2.0, 3.8, horizontal=False, color=GREEN); line(ax, [2.0, 2.0], [4.2, 5.2])
ax.text(2.5, 3.8, "flyback\ndiode", fontsize=10.5, color=GREEN, va="center")
ax.add_patch(plt.Rectangle((-0.4, 0.8), 0.8, 1.4, color=L_GREY, ec=BLACK)); ax.text(0, 1.5, "switch", ha="center", va="center", fontsize=9.5, rotation=90)
line(ax, [0, 0], [0.8, 0.2]); line(ax, [-0.4, 0.4], [0.2, 0.2], lw=3)
ax.annotate("", xy=(1.5, 4.9), xytext=(1.5, 2.7), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN, connectionstyle="arc3,rad=0"))
ax.text(1.3, 1.3, "at switch-off the coil's\ncurrent goes round\nthrough the diode", fontsize=9.5, color=GREEN)
ax.set_title("the flyback diode across the coil", fontsize=11)
ax = axes[1]
for clamp, col, lab in [(0.7, GREEN, "plain diode: switch sees 24.7 V"), (12.7, ORANGE, "diode + 12 V Zener: 36.7 V"), (24.7, RED, "diode + 24 V Zener: 48.7 V")]:
    i, t, ts, cs = 0.5, 0.0, [], []
    while t < 0.008:
        ts.append(t * 1000); cs.append(i)
        i = max(i + (-(i * 48 + clamp)) / 0.1 * 1e-6, 0.0); t += 1e-6
    ax.plot(ts, cs, color=col, lw=2.5, label=lab)
ax.set_xlabel("time after switch-off (ms)"); ax.set_ylabel("coil current (A)"); ax.grid(alpha=0.3); ax.legend(fontsize=10)
ax.set_title("a higher clamp voltage stops the current sooner", fontsize=11)
save(fig, "fig03-flyback.png")

# Figure 4: reverse polarity protection - voltage lost
fig, ax = plt.subplots(figsize=(10, 4.6))
names = ["silicon diode", "Schottky diode", "P-MOSFET\n(Chapter 88)"]
lost1 = [0.80, 0.38, 0.53 * 0.02]; lost2 = [0.95, 0.50, 3.1 * 0.02]
x = np.arange(3)
ax.bar(x - 0.2, lost1, 0.4, color=BLUE, edgecolor=BLACK, label="driving, 0.53 A")
ax.bar(x + 0.2, lost2, 0.4, color=ORANGE, edgecolor=BLACK, label="motors starting, 3.1 A")
for k in range(3):
    ax.text(k - 0.2, lost1[k] + 0.02, f"{lost1[k]:.2f}", ha="center", fontsize=10); ax.text(k + 0.2, lost2[k] + 0.02, f"{lost2[k]:.2f}", ha="center", fontsize=10)
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("volts lost (V)"); ax.grid(alpha=0.3, axis="y"); ax.legend(fontsize=10.5)
ax.set_title("protecting Rover from a reversed battery: all three block; the MOSFET wastes almost nothing", fontsize=11)
save(fig, "fig04-reverse-protection.png")

# Figure 5: solar panel with a shaded cell
fig, ax = plt.subplots(figsize=(10, 4.4))
names = ["full sun", "one cell shaded,\nno bypass diodes", "one cell shaded,\nwith bypass diodes"]
vals = [90, 18, 58]
ax.bar(range(3), vals, color=[GREEN, RED, BLUE], edgecolor=BLACK)
for k, v in enumerate(vals):
    ax.text(k, v + 2, f"{v} W", ha="center", fontsize=12)
ax.set_xticks(range(3)); ax.set_xticklabels(names); ax.set_ylabel("power (W)"); ax.set_ylim(0, 105); ax.grid(alpha=0.3, axis="y")
ax.set_title("36 cells in series: one leaf costs 80% of the power, unless bypass diodes route around it", fontsize=11)
save(fig, "fig05-solar-bypass.png")

# Figure 6: a bridge rectifier turning AC into DC, smoothed by a capacitor
fig, ax = plt.subplots(figsize=(10, 4.6))
t = np.linspace(0, 0.06, 3000)
ac = 12 * np.sin(2 * np.pi * 50 * t)
rect = np.maximum(np.abs(ac) - 1.4, 0)
vc, smooth = 0.0, []
for r in rect:
    if r > vc:
        vc = r
    else:
        vc -= 0.5 / 2200e-6 * (t[1] - t[0])
    smooth.append(vc)
ax.plot(t * 1000, ac, color=GREY, lw=1.5, label="AC in (from a coil or transformer)")
ax.plot(t * 1000, rect, color=ORANGE, lw=2, label="after the bridge of 4 diodes (always positive)")
ax.plot(t * 1000, smooth, color=BLUE, lw=2.5, label="with a 2,200 uF capacitor (0.5 A load)")
ax.axhline(0, color=BLACK, lw=1)
ax.set_xlabel("time (ms)"); ax.set_ylabel("volts"); ax.grid(alpha=0.3); ax.legend(loc="lower right", fontsize=10)
ax.set_title("rectifying: diodes flip the negative halves; a capacitor fills the gaps", fontsize=11.5)
save(fig, "fig06-rectifier.png")
print("saved 6 figures")
