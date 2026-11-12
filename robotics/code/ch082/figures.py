# Figures for Chapter 82 - LEDs and resistors.
# Run:  python figures.py      (saves PNG files in ../../images/ch082/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch082")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: an LED, its legs, and its symbol
fig, axes = plt.subplots(1, 2, figsize=(11, 5.2), gridspec_kw=dict(width_ratios=[1, 1.2]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3, 4); ax.set_ylim(-4.5, 4)
ax.add_patch(plt.Rectangle((-1, 0), 2, 2, color="#F4B6A6", ec=BLACK)); ax.add_patch(matplotlib.patches.Wedge((0, 2), 1, 0, 180, color="#F4B6A6", ec=BLACK))
ax.add_patch(plt.Rectangle((-1.2, -0.2), 2.4, 0.25, color="#F4B6A6", ec=BLACK))
ax.plot([0.95, 0.95], [-0.2, 0.05], color=BLACK, lw=2)
ax.plot([-0.5, -0.5], [-0.2, -3.8], color=GREY, lw=3); ax.plot([0.5, 0.5], [-0.2, -2.8], color=GREY, lw=3)
ax.text(-0.6, -4.2, "long leg:\nanode (+)", ha="center", fontsize=10.5, va="top")
ax.text(1.0, -3.0, "short leg:\ncathode (-)", ha="left", fontsize=10.5, va="top")
ax.annotate("flat edge on the\ncathode side", xy=(1.1, -0.1), xytext=(1.6, 1.0), fontsize=10, arrowprops=dict(arrowstyle="->"))
ax.set_title("a 5 mm LED", fontsize=11.5)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 7.5); ax.set_ylim(-2, 3)
ax.plot([0, 2.5], [0.5, 0.5], color=BLACK, lw=2); ax.add_patch(plt.Polygon([(2.5, -0.2), (2.5, 1.2), (3.7, 0.5)], color=BLACK))
ax.plot([3.7, 3.7], [-0.2, 1.2], color=BLACK, lw=3); ax.plot([3.7, 6.5], [0.5, 0.5], color=BLACK, lw=2)
for d in [0, 0.5]:
    ax.annotate("", xy=(3.9 + d, 2.2), xytext=(3.2 + d, 1.4), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=ORANGE))
ax.text(0.2, 0.9, "anode (+)", fontsize=10.5); ax.text(4.2, 0.9, "cathode (-)", fontsize=10.5)
ax.annotate("", xy=(5.9, -0.6), xytext=(0.6, -0.6), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN))
ax.text(3.2, -1.2, "conventional current flows this way only", ha="center", fontsize=10.5, color=GREEN)
ax.set_title("its symbol", fontsize=11.5)
save(fig, "fig01-led.png")

# Figure 2: I-V curves for three colours, with a resistor's load line
fig, ax = plt.subplots(figsize=(10, 5.2))
V = np.linspace(0, 5, 500)
for vf, col, lab in [(1.2, GREY, "infrared (1.2 V)"), (2.0, RED, "red (2.0 V)"), (3.1, BLUE, "blue / white (3.1 V)")]:
    I = 20 * np.exp((V - vf) / 0.052)
    ax.plot(V, np.where(I < 60, I, np.nan), color=col, lw=2.5, label=lab)
ax.plot(V, (5 - V) / 150 * 1000, color=BLACK, ls="--", lw=2, label="150 ohm from 5 V: I = (5 - V) / 150")
ax.plot(2.0, 20, "o", color=BLACK, ms=9); ax.text(2.07, 22, "red LED with 150 ohm:\n2.0 V, 20 mA", fontsize=10.5)
ax.set_xlabel("voltage across the LED (V)"); ax.set_ylabel("current (mA)"); ax.set_ylim(0, 45); ax.grid(alpha=0.3); ax.legend(fontsize=10, loc="upper right")
ax.set_title("nothing flows below the forward voltage, then the current shoots up", fontsize=11.5)
save(fig, "fig02-iv-curves.png")

# Figure 3: why a resistor - spread of current for three LEDs, with and without
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
def solve(supply, r, vf):
    lo, hi = 0.0, supply
    for _ in range(60):
        mid = (lo + hi) / 2
        if 0.020 * math.exp((mid - vf) / 0.052) > (supply - mid) / r:
            hi = mid
        else:
            lo = mid
    return (supply - lo) / r * 1000
vfs = [1.9, 2.0, 2.1]
for ax, (supply, r, title) in zip(axes, [(2.1, 0.5, "2.1 V supply, almost no resistor"), (5.0, 150.0, "5 V supply with 150 ohm")]):
    vals = [solve(supply, r, vf) for vf in vfs]
    ax.bar(range(3), vals, color=[RED, ORANGE, GREEN], edgecolor=BLACK)
    for k, v in enumerate(vals):
        ax.text(k, v + max(vals) * 0.02, f"{v:.1f} mA", ha="center", fontsize=11)
    ax.set_xticks(range(3)); ax.set_xticklabels([f"Vf {v} V" for v in vfs]); ax.set_ylabel("current (mA)")
    ax.set_title(title, fontsize=11.5); ax.grid(alpha=0.3, axis="y"); ax.set_ylim(0, max(vals) * 1.15)
fig.suptitle("three LEDs from the same bag: the resistor makes them all about 20 mA", fontsize=12, y=1.02)
save(fig, "fig03-why-resistor.png")

# Figure 4: the colour code
fig, ax = plt.subplots(figsize=(11, 5.2))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 13); ax.set_ylim(-1, 6.5)
cmap = {"black": "#000000", "brown": "#8B4513", "red": "#D62728", "orange": "#FF7F0E", "yellow": "#FFD700", "green": "#2CA02C",
        "blue": "#1F77B4", "violet": "#8A2BE2", "grey": "#808080", "white": "#FFFFFF", "gold": "#D4AF37", "silver": "#C0C0C0"}
names = list(cmap.keys())
for k, c in enumerate(names[:10]):
    ax.add_patch(plt.Rectangle((0, 5.6 - k * 0.55), 0.8, 0.45, color=cmap[c], ec=BLACK))
    ax.text(1.0, 5.82 - k * 0.55, f"{c}: {k}", va="center", fontsize=10.5)
ax.add_patch(plt.Rectangle((3.0, 5.05), 0.8, 0.45, color=cmap["gold"], ec=BLACK)); ax.text(4.0, 5.27, "gold: x0.1 or 5%", va="center", fontsize=10.5)
ax.add_patch(plt.Rectangle((3.0, 4.5), 0.8, 0.45, color=cmap["silver"], ec=BLACK)); ax.text(4.0, 4.72, "silver: x0.01 or 10%", va="center", fontsize=10.5)
# a resistor body with yellow violet red gold
ax.plot([6.0, 7.0], [2.0, 2.0], color=GREY, lw=3); ax.plot([11.0, 12.0], [2.0, 2.0], color=GREY, lw=3)
ax.add_patch(matplotlib.patches.FancyBboxPatch((7.0, 1.4), 4.0, 1.2, boxstyle="round,pad=0.1", color="#E8D4A8", ec=BLACK))
for x, c in [(7.6, "yellow"), (8.2, "violet"), (8.8, "red"), (10.3, "gold")]:
    ax.add_patch(plt.Rectangle((x, 1.35), 0.3, 1.3, color=cmap[c], ec=BLACK))
ax.text(9.0, 3.3, "yellow violet red gold", ha="center", fontsize=11)
ax.text(9.0, 0.7, "4, 7, then x100: 4,700 ohm = 4.7 kohm, +/-5%", ha="center", fontsize=11)
ax.text(9.0, 0.0, "read from the end with the bands close together;\nthe gold or silver tolerance band is at the other end", ha="center", fontsize=10)
save(fig, "fig04-colour-code.png")

# Figure 5: E12 values on a log scale
fig, ax = plt.subplots(figsize=(10, 2.8))
e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2, 10.0]
for v in e12:
    ax.plot([v, v], [0, 1], color=BLUE, lw=2.5)
    ax.text(v, 1.1, f"{v:g}", ha="center", fontsize=10.5)
for k in range(12):
    lo, hi = e12[k] * 0.9, e12[k] * 1.1
    ax.plot([lo, hi], [0.45, 0.45], color=ORANGE, lw=6, alpha=0.6)
ax.set_xscale("log"); ax.set_xlim(0.9, 11); ax.set_ylim(-0.2, 1.5); ax.set_yticks([])
ax.set_xticks([1, 2, 5, 10]); ax.set_xticklabels(["1", "2", "5", "10"])
ax.set_title("the 12 E12 values: equal steps on a log scale (x1.21 each); the orange bars show +/-10%, so together they cover every value", fontsize=10.5)
save(fig, "fig05-e12.png")

# Figure 6: Rover's status LEDs and the pin limits
fig, ax = plt.subplots(figsize=(10, 4.6))
leds = [("power\n1 k", 2.2, 1000), ("driving\n470", 3.1, 470), ("batt low\n330", 2.0, 330), ("bump L\n330", 2.1, 330),
        ("bump R\n330", 2.1, 330), ("line\n220", 2.0, 220), ("obstacle\n150", 2.0, 150)]
cur = [(4.7 - vf) / r * 1000 for _, vf, r in leds]
ax.bar(range(7), cur, color=BLUE, edgecolor=BLACK)
ax.axhline(20, color=RED, ls="--", lw=2); ax.text(6.4, 21, "per-pin limit 20 mA", ha="right", color=RED, fontsize=10.5)
for k, c in enumerate(cur):
    ax.text(k, c + 0.5, f"{c:.1f}", ha="center", fontsize=10)
ax.set_xticks(range(7)); ax.set_xticklabels([n for n, _, _ in leds], fontsize=9.5); ax.set_ylabel("current from the pin (mA)")
ax.set_ylim(0, 25); ax.grid(alpha=0.3, axis="y")
ax.set_title("Rover's status LEDs: every pin under 20 mA, 60 mA in total (30% of the chip's 200 mA)", fontsize=11)
save(fig, "fig06-pin-budget.png")
print("saved 6 figures")
