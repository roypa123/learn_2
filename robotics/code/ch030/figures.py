# Figures for Chapter 30 — Time and loops that run forever.
# Run:  python figures.py      (saves PNG files in ../../images/ch030/)
# Figure 2 is a REAL measurement, so it differs a little every time it is made.
import os
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch030")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------- Figure 1: drift and a steady schedule ----------
fig, ax = plt.subplots(figsize=(13.5, 5.2))
for k in range(0, 5):
    ax.plot([k * 20, k * 20], [0.2, 4.3], color=GREY, ls="--", lw=1)
    ax.text(k * 20, 4.45, f"{k * 20} ms", ha="center", fontsize=11.5)
t = 0
for k in range(4):
    ax.add_patch(Rectangle((t, 2.7), 5, 0.8, fc=L_ORANGE, ec=BLACK))
    ax.add_patch(Rectangle((t + 5, 2.7), 20, 0.8, fc=L_GREY, ec=BLACK))
    ax.text(t + 15, 3.1, "sleep 20", ha="center", va="center", fontsize=10.5)
    t += 25
ax.text(-2, 3.1, "work, then\nsleep 20 ms", ha="right", va="center", fontsize=12, color=RED, weight="bold")
t = 0
for k in range(4):
    ax.add_patch(Rectangle((t, 1.0), 5, 0.8, fc=L_ORANGE, ec=BLACK))
    ax.add_patch(Rectangle((t + 5, 1.0), 15, 0.8, fc=L_GREEN, ec=BLACK))
    ax.text(t + 12.5, 1.4, "sleep 15", ha="center", va="center", fontsize=10.5)
    t += 20
ax.text(-2, 1.4, "sleep only\nwhat is left", ha="right", va="center", fontsize=12, color=GREEN, weight="bold")
ax.text(40, 0.35, "orange = 5 ms of work. The top row slips further behind on every loop. The bottom row stays on the beat.", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(-18, 102); ax.set_ylim(0.1, 4.8); ax.axis("off")
save(fig, "fig01-drift-and-schedule.png")

# ---------- Figure 2: real measured periods ----------
P = 0.02
N = 50
naive = []
prev = time.perf_counter()
for i in range(N):
    time.sleep(0.005); time.sleep(P)
    now = time.perf_counter(); naive.append((now - prev) * 1000); prev = now
steady = []
start = time.perf_counter(); nxt = start + P; prev = start
for i in range(N):
    time.sleep(0.005)
    r = nxt - time.perf_counter()
    if r > 0:
        time.sleep(r)
    now = time.perf_counter(); steady.append((now - prev) * 1000); prev = now
    nxt += P
fig, ax = plt.subplots(figsize=(13, 5.0))
ax.plot(range(N), naive, "o-", color=RED, ms=4, lw=1.5, label="work, then sleep 20 ms")
ax.plot(range(N), steady, "o-", color=BLUE, ms=4, lw=1.5, label="steady loop")
ax.axhline(20, color=BLACK, ls="--", lw=2, label="wanted: 20 ms")
ax.set_xlabel("loop number"); ax.set_ylabel("measured period (ms)"); ax.grid(alpha=0.3); ax.set_ylim(15, 32); ax.legend(loc="center right", framealpha=1)
save(fig, "fig02-measured-periods.png")

# ---------- Figure 3: jobs at different rates ----------
fig, ax = plt.subplots(figsize=(13.5, 4.6))
rows = [("sensor  (0.1 s)", 0.1, BLUE, 3), ("LED  (0.25 s)", 0.25, ORANGE, 2), ("report  (0.5 s)", 0.5, GREEN, 1)]
for name, period, c, y in rows:
    ax.text(-0.03, y, name, ha="right", va="center", fontsize=12.5, weight="bold", family=MONO)
    ax.plot([0, 1], [y, y], color=L_GREY, lw=1.5, zorder=0)
    k = 0
    while k * period < 1.0 - 1e-9:
        ax.plot(k * period, y, "|", color=c, ms=30, mew=4)
        k += 1
for i in range(0, 11, 2):
    ax.text(i / 10, 0.35, f"{i / 10:.1f}", ha="center", fontsize=11.5, family=MONO)
ax.text(0.5, -0.05, "time (s). Each tick is one moment when that job runs.", ha="center", fontsize=12.5)
ax.set_xlim(-0.35, 1.05); ax.set_ylim(-0.2, 3.7); ax.axis("off")
save(fig, "fig03-jobs-at-different-rates.png")

# ---------- Figure 4: watchdog ----------
ticks = [0, 1, 2, 3, 8, 9]
fig, axes = plt.subplots(2, 1, figsize=(13, 5.4), sharex=True, gridspec_kw={"height_ratios": [1, 1.6]})
ax = axes[0]
for k in ticks:
    ax.plot(k / 10, 1, "v", color=BLUE, ms=13)
ax.axvspan(0.3, 0.8, color=L_RED)
ax.text(0.55, 1.0, "radio silent", ha="center", va="center", fontsize=13, color=RED, weight="bold")
ax.set_yticks([]); ax.set_ylabel("commands"); ax.set_ylim(0.6, 1.4)
ax = axes[1]
t = [i / 10 for i in range(11)]
out = []
last = 0.0
for i in range(11):
    if i in ticks:
        last = i / 10
    out.append(0.0 if i / 10 - last > 0.25 else 0.5)
ax.step(t, out, where="post", color=GREEN, lw=3, label="speed output")
ax.axvline(0.55, color=RED, ls="--", lw=2, label="timeout: 0.25 s after the last command")
ax.set_xlabel("time (s)"); ax.set_ylabel("speed (m/s)"); ax.set_ylim(-0.08, 0.72); ax.grid(alpha=0.3); ax.legend(loc="upper right", framealpha=1, ncol=2)
save(fig, "fig04-watchdog.png")
print("figures saved in", os.path.abspath(OUT))
