# Figures for Chapter 54 - Error, accuracy, precision and rounding in computers.
# Run:  python figures.py      (saves PNG files in ../../images/ch054/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch054")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: a toy float system with 3 bits of fraction
vals = []
for e in range(-1, 3):
    for m in range(8):
        vals.append((1 + m / 8) * 2 ** e)
fig, ax = plt.subplots(figsize=(12, 3.2))
ax.axhline(0, color=BLACK, lw=1)
for v in vals:
    ax.plot([v, v], [-0.15, 0.15], color=BLUE, lw=2)
ax.plot([0.1 * 8, 0.1 * 8], [-0.3, 0.3], color=RED, lw=0)
for x0, lab in [(0.5, "0.5"), (1, "1"), (2, "2"), (4, "4"), (8, "8")]:
    ax.text(x0, -0.45, lab, ha="center", fontsize=12)
ax.annotate("gaps of 1/16 here", (0.56, 0.17), xytext=(0.3, 0.6), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("gaps of 1/2 here", (6.5, 0.17), xytext=(5.6, 0.6), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.text(4.2, -0.85, "each blue mark is a number the computer can store exactly; everything else is rounded to the nearest mark", ha="center", fontsize=11.5)
ax.set_xlim(0, 8.3); ax.set_ylim(-1.0, 0.9); ax.axis("off")
save(fig, "fig01-float-gaps.png")

# Figure 2: accuracy against precision
random.seed(2)
fig, axes = plt.subplots(1, 4, figsize=(14, 3.9))
cases = [("accurate and precise", 0, 0, 0.08), ("precise, not accurate", 0.45, 0.3, 0.08),
         ("accurate, not precise", 0, 0, 0.35), ("neither", 0.4, -0.35, 0.35)]
for ax, (title, cx, cy, s) in zip(axes, cases):
    for r, col in [(1.0, L_GREY), (0.66, "white"), (0.33, L_GREY)]:
        ax.add_patch(Circle((0, 0), r, fc=col, ec=GREY))
    ax.plot([0], [0], "+", color=BLACK, ms=14, mew=2)
    xs = [cx + random.gauss(0, s) for _ in range(10)]; ys = [cy + random.gauss(0, s) for _ in range(10)]
    ax.plot(xs, ys, "o", color=BLUE, ms=7, mec=BLACK)
    ax.set_title(title, fontsize=12.5); ax.set_xlim(-1.1, 1.1); ax.set_ylim(-1.1, 1.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-accuracy-precision.png")

# Figure 3: clock drift
steps = np.arange(0, 3_600_001, 1000)
t32 = np.cumsum(np.full(3_600_000, np.float32(0.001), dtype=np.float32), dtype=np.float32)
true = steps * 0.001
err = np.concatenate([[0.0], (t32[999::1000].astype(float) - true[1:])])
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(true / 60, err, color=RED, lw=2.5, label="float32 sum minus true time")
ax.axhline(0, color=BLUE, lw=2.5, ls="--", label="float64 sum and integer ticks (error too small to see)")
ax.set_xlabel("true time (minutes)"); ax.set_ylabel("clock error (s)"); ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=11)
save(fig, "fig03-clock-drift.png")

# Figure 4: 16-bit counter wrapping
true_ticks = np.arange(0, 140_001, 500)
stored = (true_ticks + 32768) % 65536 - 32768
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(true_ticks / 2600, true_ticks, color=BLACK, ls="--", lw=2, label="true count")
ax.plot(true_ticks / 2600, stored, color=RED, lw=2.5, label="what a 16-bit counter holds")
ax.axhline(32767, color=GREY, ls=":", lw=1.5); ax.axhline(-32768, color=GREY, ls=":", lw=1.5)
ax.text(1, 36000, "largest 16-bit value: 32767", fontsize=11.5); ax.text(1, -40000, "smallest: -32768", fontsize=11.5)
ax.set_xlabel("distance driven (m)"); ax.set_ylabel("ticks"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig04-overflow.png")

# Figure 5: cancellation
xs = np.logspace(-9, -1, 200)
naive = 1 - np.cos(xs)
safe = 2 * np.sin(xs / 2) ** 2
rel = np.abs(naive - safe) / safe
rel[rel == 0] = 1e-18
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.loglog(xs, rel, color=RED, lw=2.5)
ax.set_xlabel("angle x (rad, log scale)"); ax.set_ylabel("relative error of 1 - cos x (log scale)"); ax.grid(alpha=0.3, which="both")
ax.text(3e-7, 0.05, "left: 100% wrong: the answer became 0", fontsize=12)
ax.set_ylim(1e-18, 10)
ax.set_yticks([1e0, 1e-3, 1e-6, 1e-9, 1e-12, 1e-15, 1e-18]); ax.set_yticklabels(["1", "1e-3", "1e-6", "1e-9", "1e-12", "1e-15", "1e-18"])
ax.set_xticks([1e-9, 1e-7, 1e-5, 1e-3, 1e-1]); ax.set_xticklabels(["1e-9", "1e-7", "1e-5", "1e-3", "0.1"])
ax.minorticks_off()
save(fig, "fig05-cancellation.png")
print("figures saved in", os.path.abspath(OUT))
