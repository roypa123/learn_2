# Figures for Chapter 83 - Switches and buttons, pull-up and pull-down resistors.
# Run:  python figures.py      (saves PNG files in ../../images/ch083/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch083")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


def zigzag(ax, x0, y0, x1, y1, color=BLACK):
    n = 6; xs, ys = [x0], [y0]; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); px, py = -dy / L, dx / L
    for k in range(1, 2 * n):
        f = k / (2 * n); s = 0.13 if k % 2 else -0.13
        xs.append(x0 + dx * f + px * s); ys.append(y0 + dy * f + py * s)
    xs.append(x1); ys.append(y1); ax.plot(xs, ys, color=color, lw=2)


# Figure 1: kinds of switches
fig, axes = plt.subplots(1, 4, figsize=(13, 3.6))
for ax in axes:
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 3.5); ax.set_ylim(-1.6, 2.0)
ax = axes[0]; line(ax, [0, 1], [0, 0]); ax.plot([1, 2.2], [0, 0], "o", color=BLACK, ms=6); line(ax, [1, 2.0], [0, 0.55]); line(ax, [2.2, 3.2], [0, 0])
ax.set_title("SPST toggle\n(on / off)", fontsize=11); ax.text(1.6, -1.0, "one pole, one throw", ha="center", fontsize=10)
ax = axes[1]; line(ax, [0, 1], [0, 0]); ax.plot(1, 0, "o", color=BLACK, ms=6); ax.plot([2.2, 2.2], [0.5, -0.5], "o", color=BLACK, ms=6)
line(ax, [1, 2.1], [0, 0.45]); line(ax, [2.2, 3.2], [0.5, 0.5]); line(ax, [2.2, 3.2], [-0.5, -0.5])
ax.text(3.3, 0.5, "A", va="center"); ax.text(3.3, -0.5, "B", va="center")
ax.set_title("SPDT\n(changeover)", fontsize=11); ax.text(1.6, -1.0, "common to A or to B", ha="center", fontsize=10)
ax = axes[2]; line(ax, [0, 1], [0, 0]); line(ax, [2.2, 3.2], [0, 0]); ax.plot([1, 2.2], [0, 0], "o", color=BLACK, ms=6)
line(ax, [0.9, 2.3], [0.35, 0.35]); line(ax, [1.6, 1.6], [0.35, 0.8]); line(ax, [1.4, 1.8], [0.8, 0.8])
ax.set_title("push button,\nnormally OPEN (NO)", fontsize=11); ax.text(1.6, -1.0, "closes while pressed", ha="center", fontsize=10)
ax = axes[3]; line(ax, [0, 1], [0, 0]); line(ax, [2.2, 3.2], [0, 0]); ax.plot([1, 2.2], [0, 0], "o", color=BLACK, ms=6)
line(ax, [0.9, 2.3], [-0.15, -0.15]); line(ax, [1.6, 1.6], [-0.15, 0.8]); line(ax, [1.4, 1.8], [0.8, 0.8])
ax.set_title("push button,\nnormally CLOSED (NC)", fontsize=11); ax.text(1.6, -1.0, "opens while pressed", ha="center", fontsize=10)
save(fig, "fig01-switch-types.png")

# Figure 2: floating input vs pulled-up input
random.seed(4)
fig, axes = plt.subplots(2, 1, figsize=(10, 5.4), sharex=True)
t = np.linspace(0, 100, 1000)
hum = 2.5 + 1.8 * np.sin(2 * np.pi * t / 20) + np.array([random.uniform(-0.6, 0.6) for _ in t])
axes[0].plot(t, hum, color=RED, lw=1.5)
axes[0].axhspan(1.5, 3.0, color=L_GREY); axes[0].text(101, 2.25, "undefined", va="center", fontsize=10)
axes[0].axhline(3.0, color=BLACK, ls=":"); axes[0].axhline(1.5, color=BLACK, ls=":")
axes[0].set_ylabel("pin (V)"); axes[0].set_ylim(-0.2, 5.4); axes[0].set_title("floating pin: it picks up 50 Hz hum and reads 0, 1, 0, 1 at random", fontsize=11)
pulled = 5.0 - np.array([random.uniform(0, 2e-6) for _ in t]) * 10e3
axes[1].plot(t, pulled, color=BLUE, lw=1.5); axes[1].axhspan(1.5, 3.0, color=L_GREY)
axes[1].axhline(3.0, color=BLACK, ls=":"); axes[1].axhline(1.5, color=BLACK, ls=":")
axes[1].set_ylabel("pin (V)"); axes[1].set_ylim(-0.2, 5.4); axes[1].set_xlabel("time (ms)")
axes[1].set_title("with a 10 kohm pull-up: a steady 5 V, always read as 1", fontsize=11)
save(fig, "fig02-floating.png")

# Figure 3: pull-up and pull-down circuits
fig, axes = plt.subplots(1, 2, figsize=(11, 5))
for ax, kind in zip(axes, ["up", "down"]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2, 7.5); ax.set_ylim(-1.2, 6.2)
    ax.text(0, 5.75, "+5V", ha="center", color=RED, fontsize=11); line(ax, [-0.4, 0.4], [5.5, 5.5]); line(ax, [0, 0], [5.5, 5.0])
    for k, w in enumerate([0.4, 0.26, 0.12]):
        line(ax, [-w, w], [-0.3 - k * 0.13, -0.3 - k * 0.13])
    line(ax, [0, 0], [0.2, -0.3])
    if kind == "up":
        zigzag(ax, 0, 5.0, 0, 3.4); line(ax, [0, 0], [3.4, 2.8]); ax.text(0.3, 4.2, "10 k\npull-up", fontsize=10.5, color=RED)
        ax.plot([0, 0], [2.0, 1.2], "o", color=BLACK, ms=6); line(ax, [0, 0], [2.8, 2.0]); line(ax, [0, 0.5], [1.2, 1.9]); line(ax, [0, 0], [1.2, 0.2])
        ax.text(0.6, 1.6, "button\nto ground", fontsize=10.5)
        ax.text(3.7, 4.4, "not pressed: 5 V -> reads 1", fontsize=10.5); ax.text(3.7, 3.8, "pressed: 0 V -> reads 0", fontsize=10.5)
        ax.text(3.7, 3.3, "('active low': pressed = 0)", fontsize=10.5, color=BLUE)
        ax.set_title("pull-UP", fontsize=12)
    else:
        ax.plot([0, 0], [4.8, 4.0], "o", color=BLACK, ms=6); line(ax, [0, 0], [5.0, 4.8]); line(ax, [0, 0.5], [4.0, 4.7]); line(ax, [0, 0], [4.0, 2.8])
        ax.text(0.6, 4.4, "button\nto +5V", fontsize=10.5)
        line(ax, [0, 0], [2.8, 2.2]); zigzag(ax, 0, 2.2, 0, 0.6); line(ax, [0, 0], [0.6, 0.2]); ax.text(0.3, 1.4, "10 k\npull-down", fontsize=10.5, color=RED)
        ax.text(3.7, 4.4, "not pressed: 0 V -> reads 0", fontsize=10.5); ax.text(3.7, 3.8, "pressed: 5 V -> reads 1", fontsize=10.5)
        ax.text(3.7, 3.3, "('active high': pressed = 1)", fontsize=10.5, color=BLUE)
        ax.set_title("pull-DOWN", fontsize=12)
    ax.plot(0, 2.8, "o", color=BLACK, ms=7); line(ax, [0, 2.0], [2.8, 2.8], color=BLUE); ax.text(2.1, 2.8, "to the\ninput pin", va="center", fontsize=10, color=BLUE)
save(fig, "fig03-pull-up-down.png")

# Figure 4: choosing the pull-up value
fig, ax1 = plt.subplots(figsize=(10, 4.8))
R = np.logspace(2.5, 7, 200)
ax1.loglog(R, 5 / R * 1000, color=RED, lw=2.5, label="current when pressed (mA)")
ax1.set_xlabel("pull-up resistance (ohm)"); ax1.set_ylabel("current when pressed (mA)", color=RED)
ax2 = ax1.twinx()
ax2.semilogx(R, np.maximum(5 - 1e-6 * R, 0), color=BLUE, lw=2.5, label="pin voltage with 1 uA leakage (V)")
ax2.axhline(3.0, color=BLUE, ls=":"); ax2.text(3.5e2, 3.1, "HIGH threshold 3 V", color=BLUE, fontsize=10)
ax2.set_ylabel("pin voltage, switch open (V)", color=BLUE); ax2.set_ylim(0, 5.5)
ax1.axvspan(4.7e3, 1e5, color=L_GREEN, alpha=0.5); ax1.text(2.2e4, 3.0, "good:\n4.7 k to 100 k", ha="center", fontsize=10.5)
ax1.set_xticks([1e3, 1e4, 1e5, 1e6, 1e7]); ax1.set_xticklabels(["1 k", "10 k", "100 k", "1 M", "10 M"])
ax1.set_yticks([0.001, 0.01, 0.1, 1, 10]); ax1.set_yticklabels(["0.001", "0.01", "0.1", "1", "10"])
ax1.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax1.grid(alpha=0.3, which="both"); ax1.set_title("too small wastes current; too big lets leakage and noise win", fontsize=11.5)
save(fig, "fig04-choosing-r.png")

# Figure 5: bounce and debounce
random.seed(7)
changes = [(0.0, 1)]; t0 = 2.0; tt = t0; st = 0
while tt < t0 + 4.0:
    changes.append((tt, st)); tt += random.uniform(0.05, 0.6) * (1 - (tt - t0) / 4.0) + 0.02; st = 1 - st
changes.append((tt, 0))
ts = np.arange(0, 12, 0.1)
lv = []
for x in ts:
    s = 1
    for when, state in changes:
        if when <= x:
            s = state
    lv.append(s)
lv = np.array(lv)
deb = np.ones_like(lv); acc, run, last = 1, 0, 1
for k, s in enumerate(lv):
    run = run + 1 if s == last else 1; last = s
    if run >= 50 and s != acc:
        acc = s
    deb[k] = acc
fig, axes = plt.subplots(2, 1, figsize=(10, 4.8), sharex=True)
axes[0].step(ts, lv * 5, where="post", color=RED, lw=2); axes[0].set_ylabel("pin (V)"); axes[0].set_ylim(-0.5, 5.8)
axes[0].set_title("one press: the contacts bounce for about 4 ms (12 falling edges)", fontsize=11)
axes[1].step(ts, deb, where="post", color=GREEN, lw=2.5); axes[1].set_ylabel("debounced"); axes[1].set_ylim(-0.2, 1.3)
axes[1].set_xlabel("time (ms)"); axes[1].set_title("debounced: accept a change only after 5 ms of steady readings (1 press)", fontsize=11)
save(fig, "fig05-bounce.png")

# Figure 6: NO vs NC bumper with a broken wire
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
cases = ["clear,\nwire ok", "hit,\nwire ok", "clear,\nwire broken", "hit,\nwire broken"]
no = [0, 1, 0, 0]; nc = [0, 1, 1, 1]
for ax, vals, title in zip(axes, [no, nc], ["normally-OPEN bumper", "normally-CLOSED bumper"]):
    truth = [0, 1, 0, 1]
    cols = [GREEN if v == tr else (RED if tr == 1 else GREY) for v, tr in zip(vals, truth)]
    ax.bar(range(4), [1] * 4, color=cols, edgecolor=BLACK)
    for k, v in enumerate(vals):
        ax.text(k, 0.5, "HIT" if v else "clear", ha="center", va="center", fontsize=11, color="white", fontweight="bold")
    ax.set_xticks(range(4)); ax.set_xticklabels(cases, fontsize=9.5); ax.set_yticks([]); ax.set_title(title, fontsize=11.5)
axes[0].text(2.0, 1.12, "red: a real hit goes unseen (dangerous)", ha="center", fontsize=10, color=RED)
axes[1].text(2.0, 1.12, "grey: a false alarm, the robot stops (safe)", ha="center", fontsize=10, color=BLACK)
for ax in axes:
    ax.set_ylim(0, 1.3)
save(fig, "fig06-fail-safe.png")
print("saved 6 figures")
