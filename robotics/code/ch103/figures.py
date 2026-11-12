# Figures for Chapter 103 - Timing without delay: millis().
# Run:  python figures.py      (saves PNG files in ../../images/ch103/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Wedge

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch103")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


# Figure 1: when does each sketch look at the button?
downs = [700, 1650, 2400, 3300, 4150, 5050, 5800, 6900]
fig, ax = plt.subplots(figsize=(12, 4.0))
for row, label in [(1, "delay_blind.ino:\nreads once a second"), (0, "blink_millis.ino:\nreads all the time")]:
    for d in downs:
        ax.add_patch(Rectangle((d, row + 0.15), 150, 0.7, fc=L_ORANGE, ec=ORANGE))
    ax.text(-150, row + 0.5, label, ha="right", va="center", fontsize=10.5)
for k in range(1, 9):
    t = 1000 * k
    hit = any(d <= t < d + 150 for d in downs)
    ax.plot([t, t], [1.05, 1.95], color=GREEN if hit else GREY, lw=3 if hit else 1.5)
ax.add_patch(Rectangle((0, 0.45), 8000, 0.1, fc=GREEN, ec="none", alpha=0.6))
ax.text(4000, -0.25, "orange: the 8 presses (150 ms each). Lines: the moments the button is read; green = a press seen", ha="center", fontsize=10.5)
ax.set_xlim(0, 8000); ax.set_ylim(-0.5, 2.1); ax.set_yticks([]); ax.set_xlabel("time (ms)")
save(fig, "fig01-who-sees-presses.png")

# Figure 2: the shape of a loop that never waits
fig, ax = plt.subplots(figsize=(12, 5.2))
box(ax, 0.2, 2.2, 2.0, 0.9, "loop() starts", L_GREY)
jobs = [("LED: 250 ms\nsince last?", "toggle LED,\nlast += 250"), ("sensor: 100 ms\nsince last?", "read sensor,\nlast += 100"),
        ("report: 1000 ms\nsince last?", "print, reset,\nlast += 1000")]
for k, (q, a) in enumerate(jobs):
    x = 2.9 + k * 2.9
    box(ax, x, 2.2, 2.2, 0.9, q, L_BLUE, fs=10)
    box(ax, x, 0.4, 2.2, 0.9, a, L_GREEN, fs=10)
    ax.add_patch(FancyArrowPatch((x + 1.1, 2.15), (x + 1.1, 1.35), arrowstyle="-|>", mutation_scale=14, color=GREEN, lw=1.8))
    ax.text(x + 1.2, 1.7, "yes", fontsize=10, color=GREEN)
    ax.add_patch(FancyArrowPatch((x - 0.65, 2.65), (x - 0.05, 2.65), arrowstyle="-|>", mutation_scale=14, color=BLACK, lw=1.8))
    ax.text(x - 0.62, 2.8, "no" if k else "", fontsize=10, color=RED)
box(ax, 11.6, 2.2, 1.6, 0.9, "loop() ends\n(microseconds)", L_GREY, fs=10)
ax.add_patch(FancyArrowPatch((11.15, 2.65), (11.55, 2.65), arrowstyle="-|>", mutation_scale=14, color=BLACK, lw=1.8))
ax.annotate("", xy=(1.2, 3.15), xytext=(12.4, 3.15), arrowprops=dict(arrowstyle="-|>", lw=1.8, connectionstyle="arc3,rad=0.25"))
ax.text(6.8, 4.62, "and again, about 200,000 times a second", ha="center", fontsize=11)
ax.text(6.8, 0.0, "each check takes about a microsecond; a job only runs when it is due; nothing ever waits", ha="center", fontsize=11, color=BLUE)
ax.set_xlim(0, 13.4); ax.set_ylim(-0.3, 4.9); ax.axis("off")
save(fig, "fig02-never-wait.png")

# Figure 3: when each of the three jobs runs during the first second
fig, ax = plt.subplots(figsize=(12, 3.6))
for row, (name, period, col) in enumerate([("LED (250 ms)", 250, BLUE), ("sensor (100 ms)", 100, GREEN), ("report (1000 ms)", 1000, RED)]):
    y = 2 - row
    for t in range(period, 1001, period):
        ax.plot([t, t], [y - 0.3, y + 0.3], color=col, lw=3)
    ax.text(-15, y, name, ha="right", va="center", fontsize=11)
ax.set_xlim(0, 1050); ax.set_ylim(-0.6, 2.6); ax.set_yticks([]); ax.set_xlabel("time (ms)")
ax.set_title("each mark is one run of a job; between them, loop() spins about 200,000 times a second doing nothing but checking", fontsize=10.5)
save(fig, "fig03-three-jobs.png")

# Figure 4: drift - last = millis() against last += interval (the model of drift.ino)
t, lastA, lastB = 0, 0, 0
runsA, runsB, timesA, timesB = [], [], [], []
while t < 10000:
    t += 7
    if t - lastA >= 100:
        lastA = t; timesA.append(t)
    if t - lastB >= 100:
        lastB += 100; timesB.append(t)
fig, axes = plt.subplots(2, 1, figsize=(11, 6))
for ax, times, col, name in [(axes[0], timesA, RED, "A: last = millis()"), (axes[1], timesB, BLUE, "B: last += 100")]:
    ax.plot(range(1, len(times) + 1), [ti - 100 * (k + 1) for k, ti in enumerate(times)], "o-", color=col, ms=3, lw=1.5)
    ax.set_title(f"{name}: {len(times)} runs in 10 s", fontsize=11)
    ax.set_ylabel("late against\nthe 100 ms grid (ms)"); ax.grid(alpha=0.3)
axes[1].set_xlabel("run number"); axes[1].set_ylim(-5, 20)
fig.tight_layout()
save(fig, "fig04-drift.png")

# Figure 5: subtraction across the wrap
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.add_patch(Wedge((0, 0), 1.0, 0, 360, width=0.15, fc=L_BLUE, ec=BLACK))
for value, ang, text in [(0, 90, "0"), (1, 110, "4,294,966,296\n(last)"), (2, 72, "500\n(now)")]:
    a = math.radians(ang)
    ax.plot([0.85 * math.cos(a), math.cos(a)], [0.85 * math.sin(a), math.sin(a)], color=RED if value else BLACK, lw=2.5 if value else 1.5)
    ax.text(1.3 * math.cos(a), 1.3 * math.sin(a), text, ha="center", va="center", fontsize=11)
ax.add_patch(FancyArrowPatch((0.75 * math.cos(math.radians(108)), 0.75 * math.sin(math.radians(108))),
                             (0.75 * math.cos(math.radians(74)), 0.75 * math.sin(math.radians(74))),
                             connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=16, color=GREEN, lw=2.5))
ax.text(0, 0.45, "now - last = 1,500", ha="center", fontsize=12, color=GREEN, weight="bold")
ax.text(0, 0.1, "unsigned subtraction goes the short way\nround the circle, through the wrap", ha="center", fontsize=11)
ax.text(0, -0.45, "millis() counts 0 ... 4,294,967,295,\nthen starts again at 0 (49.7 days)", ha="center", fontsize=11, color=GREY)
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.3, 1.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-wrap.png")

# Figure 6: the delay loop against the steady loop (the models of loop_delay.ino and loop_steady.ino)
work = 2.24
starts_d = [k * (10 + work) for k in range(45)]
starts_s, nxt = [], 0.0
t = 0.0
for k in range(45):
    t = max(t, nxt)
    starts_s.append(t)
    nxt += 10
    t += work + (12 if k == 25 else 0)
fig, ax = plt.subplots(figsize=(12, 4.2))
for row, (starts, col, name) in enumerate([(starts_d, RED, "delay(10)"), (starts_s, BLUE, "steady (micros)")]):
    y = 1 - row
    for k, s in enumerate(starts):
        w = work + (12 if (row == 1 and k == 25) else 0)
        ax.add_patch(Rectangle((s, y + 0.1), w, 0.6, fc=col, ec="none"))
    ax.text(-8, y + 0.4, name, ha="right", va="center", fontsize=11)
for g in range(0, 451, 10):
    ax.axvline(g, color=L_GREY, lw=0.8, zorder=0)
ax.annotate("one step takes 12 ms longer:\nthe next starts late, then the\nschedule is back on the grid", xy=(266, 0.75), xytext=(300, 1.2),
            fontsize=10, arrowprops=dict(arrowstyle="-|>", color=BLACK))
ax.set_xlim(0, 450); ax.set_ylim(-0.2, 1.9); ax.set_yticks([]); ax.set_xlabel("time (ms); grey lines every 10 ms")
save(fig, "fig06-two-loops.png")

# Figure 7: how quickly Rover notices a bump while its red light flashes
fig, ax = plt.subplots(figsize=(10, 4))
names = ["Chapter 98:\nflashing with delay()", "this chapter:\nflashing with millis()"]
vals = [1000.0, 0.046]
ax.barh(names, vals, color=[RED, GREEN])
ax.set_xscale("log"); ax.set_xticks([0.01, 0.1, 1, 10, 100, 1000]); ax.set_xticklabels(["0.01", "0.1", "1", "10", "100", "1,000"])
ax.text(1000 * 0.6, 0, "up to 1,000 ms", va="center", ha="right", fontsize=11, color="white")
ax.text(0.06, 1, "0.046 ms", va="center", fontsize=11)
ax.set_xlabel("worst time before a bump is noticed (ms, log scale)"); ax.set_xlim(0.01, 3000)
save(fig, "fig07-reaction.png")
print("figures saved in", os.path.abspath(OUT))
