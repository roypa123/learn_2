# Figures for Chapter 31 — Random numbers: simulating noisy sensors.
# Run:  python figures.py      (saves PNG files in ../../images/ch031/)
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch031")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------- Figure 1: uniform and bell curve ----------
random.seed(10)
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
ax = axes[0]
ax.hist([random.uniform(0.4, 0.6) for _ in range(20000)], bins=40, color=L_ORANGE, ec=ORANGE)
ax.set_title("random.uniform(0.4, 0.6): every value equally likely"); ax.set_xlabel("value"); ax.set_ylabel("how many times")
ax = axes[1]
ax.hist([random.gauss(0.5, 0.03) for _ in range(20000)], bins=60, color=L_BLUE, ec=BLUE)
ax.axvline(0.5, color=BLACK, ls="--", lw=2)
ax.set_title("random.gauss(0.5, 0.03): most values near the middle"); ax.set_xlabel("value")
ax.axvspan(0.47, 0.53, color=L_GREEN, alpha=0.5, zorder=0, label="within 1 standard deviation: 68%")
ax.legend(loc="upper left", fontsize=10.5, framealpha=1)
save(fig, "fig01-two-kinds-of-random.png")

# ---------- Figure 2: a noisy sensor ----------
random.seed(1)
vals = []
for _ in range(120):
    if random.random() < 0.03:
        vals.append(0.0)
    else:
        vals.append(0.50 + random.gauss(0, 0.01))
fig, ax = plt.subplots(figsize=(13, 4.8))
ax.plot(range(120), vals, "o-", color=BLUE, ms=3.5, lw=1, label="readings")
ax.axhline(0.50, color=BLACK, ls="--", lw=2, label="true distance 0.50 m")
for i, v in enumerate(vals):
    if v == 0.0:
        ax.plot(i, v, "v", color=RED, ms=11)
ax.plot([], [], "v", color=RED, label="failed reading (dropout)")
ax.set_xlabel("reading number"); ax.set_ylabel("distance (m)"); ax.grid(alpha=0.3); ax.legend(loc="center right", framealpha=1)
save(fig, "fig02-noisy-sensor.png")

# ---------- Figure 3: averaging reduces noise ----------
ns = [1, 4, 16, 64]
measured = [9.78, 4.97, 2.51, 1.25]
fig, ax = plt.subplots(figsize=(10.5, 5.0))
xs = list(range(1, 65))
ax.plot(xs, [10 / n ** 0.5 for n in xs], color=GREY, lw=2, label="prediction: noise / square root of N")
ax.plot(ns, measured, "o", color=BLUE, ms=11, label="measured (2000 tries each)")
for n, m in zip(ns, measured):
    ax.annotate(f"{m} mm", xy=(n, m), xytext=(n + 1.5, m + 0.5), fontsize=12)
ax.set_xlabel("number of readings averaged (N)"); ax.set_ylabel("spread (mm)"); ax.set_ylim(0, 11.5); ax.grid(alpha=0.3); ax.legend(framealpha=1)
save(fig, "fig03-averaging-reduces-noise.png")

# ---------- Figure 4: the distribution of closest approaches ----------
random.seed(3)


def one_run(gain, noise_m=0.03):
    d, closest = 1.0, 1.0
    for _ in range(20):
        m = d + random.gauss(0, noise_m)
        v = max(-0.25, min(0.25, gain * (m - 0.30)))
        d -= v * 0.5
        closest = min(closest, d)
    return closest


fig, ax = plt.subplots(figsize=(13, 5.0))
for gain, c in [(1.0, BLUE), (2.0, ORANGE), (3.0, RED)]:
    ax.hist([one_run(gain) for _ in range(500)], bins=30, histtype="step", lw=2.8, color=c, label=f"gain {gain}")
ax.axvline(0.30, color=BLACK, ls="--", lw=2, label="setpoint 0.30 m")
ax.axvline(0.25, color=RED, ls=":", lw=2.5, label="near-miss limit 0.25 m")
ax.set_xlabel("closest distance reached in one run (m)"); ax.set_ylabel("number of runs (out of 500)"); ax.grid(alpha=0.3); ax.legend(framealpha=1, loc="upper left")
save(fig, "fig04-closest-approach.png")

# ---------- Figure 5: random cleaning ----------
steps = [100, 400, 1600, 6400]
cov = [11, 32, 74, 99]
fig, ax = plt.subplots(figsize=(10.5, 5.0))
ax.plot(steps, cov, "o-", color=BLUE, lw=2.5, ms=10, label="wandering at random")
ax.plot([400, 400], [0, 100], color=GREY, ls="--", lw=1.5)
ax.plot([399], [100], "s", color=GREEN, ms=12, label="back-and-forth path: 100% in 399 moves")
ax.annotate("random: only 32% after 400 steps", xy=(400, 32), xytext=(900, 22), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.set_xscale("log"); ax.set_xticks(steps); ax.set_xticklabels([str(s) for s in steps]); ax.minorticks_off(); ax.set_xlabel("steps (each mark is 4 times the last)"); ax.set_ylabel("floor cleaned (%)"); ax.grid(alpha=0.3); ax.legend(framealpha=1, loc="lower right")
ax.set_ylim(0, 108)
save(fig, "fig05-random-cleaning.png")
print("figures saved in", os.path.abspath(OUT))
