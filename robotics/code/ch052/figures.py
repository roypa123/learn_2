# Figures for Chapter 52 - Exponentials and logarithms.
# Run:  python figures.py      (saves PNG files in ../../images/ch052/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch052")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: adding the same amount against multiplying by the same factor
steps = np.arange(0, 11)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(steps, 1 + 10 * steps, "o--", color=GREEN, lw=2.5, ms=7, label="add 10 each step (straight line)")
ax.plot(steps, 2.0 ** steps, "s-", color=BLUE, lw=3, ms=7, label="double each step (exponential)")
ax.annotate("1024", (10, 1024), xytext=(7.3, 900), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("101", (10, 101), xytext=(8.4, 260), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("step"); ax.set_ylabel("value"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
save(fig, "fig01-add-vs-multiply.png")

# Figure 2: exponential decay with time constant markers
tau = 1.0
t = np.linspace(0, 5, 300)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, np.exp(-t / tau), color=BLUE, lw=3, label="share left = e to the power (-t / tau)")
for k in range(1, 5):
    v = math.exp(-k)
    ax.plot([k, k], [0, v], color=GREY, ls=":", lw=1.5); ax.plot([k], [v], "o", color=RED, ms=8)
    ax.text(k + 0.05, v + 0.03, f"{v:.1%}", fontsize=12, color=RED)
ax.set_xticks(range(0, 6)); ax.set_xticklabels(["0", "1 tau", "2 tau", "3 tau", "4 tau", "5 tau"])
ax.set_xlabel("time"); ax.set_ylabel("share of the starting gap"); ax.grid(alpha=0.3); ax.legend(loc="upper right")
save(fig, "fig02-decay.png")

# Figure 3: (1 + 1/n)^n approaching e
ns = np.unique(np.logspace(0, 4, 40).astype(int))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(ns, (1 + 1 / ns) ** ns, "o-", color=BLUE, lw=2.5, ms=6, label="(1 + 1/n) to the power n")
ax.axhline(math.e, color=BLACK, ls="--", lw=2, label="e = 2.71828...")
ax.set_xscale("log"); ax.set_xticks([1, 10, 100, 1000, 10000]); ax.set_xticklabels(["1", "10", "100", "1,000", "10,000"])
ax.set_xlabel("number of pieces n (log scale)"); ax.set_ylabel("total growth factor"); ax.grid(alpha=0.3); ax.legend(loc="lower right")
ax.set_ylim(1.9, 2.85)
save(fig, "fig03-find-e.png")

# Figure 4: linear against log scale
names = ["thermostat", "vacuum", "warehouse", "factory arm", "drone"]
rates = [0.2, 50, 100, 1000, 2000]
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, logy in zip(axes, [False, True]):
    ax.bar(names, rates, color=[GREY, ORANGE, BLUE, GREEN, RED], edgecolor=BLACK)
    ax.tick_params(axis="x", labelrotation=20)
    ax.grid(axis="y", alpha=0.3)
axes[0].set_title("ordinary scale: small values vanish", fontsize=13); axes[0].set_ylabel("loops per second")
axes[1].set_yscale("log"); axes[1].set_ylim(0.05, 20000)
axes[1].set_yticks([0.1, 1, 10, 100, 1000, 10000]); axes[1].set_yticklabels(["0.1", "1", "10", "100", "1,000", "10,000"])
axes[1].set_title("log scale: each grid line is 10 times the one below", fontsize=13)
save(fig, "fig04-log-scale.png")

# Figure 5: EMA filter
random.seed(4)
dt, alpha = 0.02, 0.1
ts, tr, rd, sm = [], [], [], []
s = 1.0
for i in range(0, 76):
    tt = i * dt
    true = 1.0 if tt < 0.2 else 0.6
    r = true + random.gauss(0, 0.03)
    s = s + alpha * (r - s)
    ts.append(tt); tr.append(true); rd.append(r); sm.append(s)
tau = -dt / math.log(1 - alpha)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ts, rd, ".", color=GREY, ms=7, label="noisy readings")
ax.plot(ts, tr, color=BLACK, ls="--", lw=2, label="true distance")
ax.plot(ts, sm, color=BLUE, lw=3, label="smoothed output")
target = 1.0 - 0.632 * 0.4
ax.plot([0.2 + tau], [target], "o", color=RED, ms=10, zorder=5)
ax.annotate(f"63% of the way after tau = {tau:.2f} s", (0.2 + tau, target), xytext=(0.5, 0.82), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("time (s)"); ax.set_ylabel("distance (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=11)
save(fig, "fig05-ema.png")

# Figure 6: motor cooling
t = np.linspace(0, 1500, 300)
T = 25 + 65 * np.exp(-t / 300)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, T, color=BLUE, lw=3, label="motor temperature")
ax.axhline(25, color=GREY, ls=":", lw=2); ax.text(1100, 21.5, "room: 25 C", fontsize=12)
ax.axhline(50, color=RED, ls="--", lw=2); ax.text(1000, 52, "safe to restart: 50 C", fontsize=12, color=RED)
ax.plot([286.7], [50], "o", color=RED, ms=11); ax.annotate("after 287 s", (286.7, 50), xytext=(380, 68), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("time since the motor stopped (s)"); ax.set_ylabel("temperature (C)"); ax.grid(alpha=0.3); ax.legend(loc="upper right"); ax.set_ylim(19, 93)
save(fig, "fig06-cooling.png")
print("figures saved in", os.path.abspath(OUT))
