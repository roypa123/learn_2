# Figures for Chapter 40 - Algebra part 1.
# Run:  python figures.py      (saves PNG files in ../../images/ch040/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch040")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: a letter is a labelled box
fig, ax = plt.subplots(figsize=(11, 3.6))
for i, (label, value, face) in enumerate([("v (speed)", "0.4", L_BLUE), ("t (time)", "30", L_GREEN), ("d (distance)", "?", L_ORANGE)]):
    x = i * 3.8
    ax.add_patch(FancyBboxPatch((x, 0.4), 2.4, 1.6, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.3))
    ax.text(x + 1.2, 1.2, value, ha="center", va="center", fontsize=25, weight="bold")
    ax.text(x + 1.2, 2.3, label, ha="center", fontsize=13.5)
ax.text(3.1, 1.2, "x", fontsize=20, ha="center", va="center")
ax.text(6.9, 1.2, "=", fontsize=20, ha="center", va="center")
ax.set_xlim(-0.2, 10.4); ax.set_ylim(0.2, 2.8); ax.axis("off")
save(fig, "fig01-letter-box.png")

# Figure 2: balance scale for 3x + 2 = 14
fig, ax = plt.subplots(figsize=(11, 5.0))
ax.add_patch(Polygon([(4.7, 0), (5.3, 0), (5, 3.5)], closed=True, fc=L_GREY, ec=BLACK))
ax.plot([1, 9], [3.5, 3.5], color=BLACK, lw=4)
for cx in (2.0, 8.0):
    ax.plot([cx, cx], [3.5, 2.1], color=BLACK, lw=1.5, zorder=1)
    ax.plot([cx - 1.7, cx + 1.7], [2.1, 2.1], color=BLACK, lw=4)
for i in range(3):
    ax.add_patch(Rectangle((0.5 + i * 0.75, 2.15), 0.65, 0.65, fc=L_BLUE, ec=BLACK, zorder=3))
    ax.text(0.825 + i * 0.75, 2.47, "x", ha="center", va="center", fontsize=14, zorder=4)
for i in range(2):
    ax.add_patch(Rectangle((2.8 + i * 0.42, 2.15), 0.38, 0.38, fc=L_ORANGE, ec=BLACK, zorder=3))
    ax.text(2.99 + i * 0.42, 2.34, "1", ha="center", va="center", fontsize=10, zorder=4)
for r in range(2):
    for i in range(7):
        ax.add_patch(Rectangle((6.5 + i * 0.43, 2.15 + r * 0.43), 0.39, 0.39, fc=L_ORANGE, ec=BLACK, zorder=3))
        ax.text(6.695 + i * 0.43, 2.345 + r * 0.43, "1", ha="center", va="center", fontsize=10, zorder=4)
ax.text(2.0, 3.8, "3x + 2", ha="center", fontsize=17, weight="bold")
ax.text(8.0, 3.8, "14", ha="center", fontsize=17, weight="bold")
ax.text(5, -0.45, "Both sides weigh the same. That is what the = sign says.", ha="center", fontsize=13)
ax.set_xlim(0, 10); ax.set_ylim(-0.7, 4.5); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-balance.png")

# Figure 3: area pictures for the two expansions
fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
ax = axes[0]
ax.add_patch(Rectangle((0, 0), 3, 2, fc=L_BLUE, ec=BLACK)); ax.add_patch(Rectangle((3, 0), 2, 2, fc=L_GREEN, ec=BLACK))
ax.text(1.5, 1, "c x a", ha="center", va="center", fontsize=15); ax.text(4, 1, "c x b", ha="center", va="center", fontsize=15)
ax.text(1.5, 2.15, "a", ha="center", fontsize=14); ax.text(4, 2.15, "b", ha="center", fontsize=14); ax.text(-0.2, 1, "c", ha="right", va="center", fontsize=14)
ax.set_title("c(a + b) = ca + cb", fontsize=15); ax.set_xlim(-0.6, 5.3); ax.set_ylim(-0.2, 5.3); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
a, b = 3, 2
ax.add_patch(Rectangle((0, b), a, a, fc=L_BLUE, ec=BLACK)); ax.add_patch(Rectangle((a, b), b, a, fc=L_GREEN, ec=BLACK))
ax.add_patch(Rectangle((0, 0), a, b, fc=L_GREEN, ec=BLACK)); ax.add_patch(Rectangle((a, 0), b, b, fc=L_ORANGE, ec=BLACK))
ax.text(1.5, 3.5, "a x a", ha="center", va="center", fontsize=15); ax.text(4, 3.5, "a x b", ha="center", va="center", fontsize=15)
ax.text(1.5, 1, "a x b", ha="center", va="center", fontsize=15); ax.text(4, 1, "b x b", ha="center", va="center", fontsize=15)
ax.text(1.5, 5.15, "a", ha="center", fontsize=14); ax.text(4, 5.15, "b", ha="center", fontsize=14)
ax.text(-0.2, 3.5, "a", ha="right", va="center", fontsize=14); ax.text(-0.2, 1, "b", ha="right", va="center", fontsize=14)
ax.set_title("(a + b)(a + b) = a x a + 2 x a x b + b x b", fontsize=15); ax.set_xlim(-0.6, 5.3); ax.set_ylim(-0.2, 5.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-area-models.png")

# Figure 4: time and energy parts of a mission
waits = [0, 5, 10, 20, 40]
drive = 60 * (800 / 1.2) / 3600
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.bar(range(5), [drive] * 5, color=BLUE, label="driving part: P_d x d / v")
wait = [15 * w * 60 / 3600 for w in waits]
ax.bar(range(5), wait, bottom=[drive] * 5, color=GREEN, hatch="//", edgecolor="white", label="waiting part: P_w x t_w")
for i, w in enumerate(wait):
    ax.text(i, drive + w + 0.3, f"{drive + w:.1f}", ha="center", fontsize=12)
ax.set_xticks(range(5)); ax.set_xticklabels([f"{w} min" for w in waits]); ax.set_xlabel("waiting time at the door"); ax.set_ylabel("energy for one trip (Wh)")
ax.set_ylim(0, 25); ax.grid(alpha=0.3, axis="y"); ax.legend(loc="upper left")
save(fig, "fig04-energy-parts.png")

# Figure 5: cycle time and speed
sp = [0.75, 1.5, 3.0, 6.0]
move = [2 * 0.6 / s for s in sp]
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.bar(range(4), move, color=BLUE, label="moving: 2L / v")
ax.bar(range(4), [0.6] * 4, bottom=move, color=GREY, hatch="\\\\", edgecolor="white", label="gripping: 2g")
for i, m in enumerate(move):
    ax.text(i, m + 0.6 + 0.05, f"{m + 0.6:.1f} s", ha="center", fontsize=12.5)
ax.set_xticks(range(4)); ax.set_xticklabels([f"{s} m/s" for s in sp]); ax.set_xlabel("arm speed"); ax.set_ylabel("time for one cycle (s)")
ax.set_ylim(0, 2.9); ax.grid(alpha=0.3, axis="y"); ax.legend()
save(fig, "fig05-cycle-time.png")
print("figures saved in", os.path.abspath(OUT))
