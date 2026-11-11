# Figures for Chapter 58 - Acceleration.
# Run:  python figures.py      (saves PNG files in ../../images/ch058/)
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch058")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: velocity-time graph and acceleration-time graph of the same trip
t = [0, 1, 2, 3, 4, 5, 6, 7, 8]
v = [0, 0.5, 1.0, 1.5, 1.5, 1.5, 0.9, 0.3, 0.0]
a = [0.5, 0.5, 0.5, 0, 0, -0.6, -0.6, -0.3]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7.5), sharex=True)
ax1.plot(t, v, "o-", color=BLUE, lw=3, ms=7)
ax1.text(1.2, 1.15, "slope +0.5 m/s^2\n(speeding up)", fontsize=11.5, color=GREEN, ha="center")
ax1.text(4.0, 1.65, "slope 0 (steady)", fontsize=11.5, ha="center")
ax1.text(6.9, 1.05, "slope -0.6 m/s^2\n(slowing down)", fontsize=11.5, color=RED, ha="center")
ax1.set_ylabel("velocity v (m/s)"); ax1.set_ylim(-0.1, 2.0); ax1.grid(alpha=0.3)
for i in range(8):
    col = GREEN if a[i] > 0 else (RED if a[i] < 0 else GREY)
    ax2.fill_between([t[i], t[i + 1]], [0, 0], [a[i], a[i]], color=col, alpha=0.35)
    ax2.plot([t[i], t[i + 1]], [a[i], a[i]], color=col, lw=3)
ax2.axhline(0, color=BLACK, lw=1)
ax2.text(1.5, 0.22, "area = 0.5 x 3 = +1.5 m/s", ha="center", fontsize=11.5)
ax2.text(6.5, -0.48, "area = -1.2 - 0.3 = -1.5 m/s", ha="center", fontsize=11.5)
ax2.set_ylabel("acceleration a (m/s^2)"); ax2.set_xlabel("time t (s)"); ax2.set_ylim(-0.8, 0.75); ax2.grid(alpha=0.3)
save(fig, "fig01-v-and-a.png")

# Figure 2: the four sign cases
fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), sharex=True, sharey=True)
tt = np.array([0, 4])
cases = [(0.2, 0.25, "v > 0, a > 0:\nforwards, speeding up", GREEN),
         (1.2, -0.25, "v > 0, a < 0:\nforwards, slowing down", RED),
         (-0.2, -0.25, "v < 0, a < 0:\nbackwards, speeding up", GREEN),
         (-1.2, 0.25, "v < 0, a > 0:\nbackwards, slowing down", RED)]
for ax, (v0, acc, txt, col) in zip(axes.flat, cases):
    ax.plot(tt, v0 + acc * tt, color=BLUE, lw=3)
    ax.axhline(0, color=BLACK, lw=1)
    ax.set_title(txt, fontsize=12, color=col)
    ax.grid(alpha=0.3); ax.set_ylim(-1.5, 1.5)
for ax in axes[1]:
    ax.set_xlabel("time (s)")
for ax in axes[:, 0]:
    ax.set_ylabel("velocity (m/s)")
fig.tight_layout()
save(fig, "fig02-sign-cases.png")

# Figure 3: ramp limiter
DT, MA, MD = 0.1, 0.8, 1.2
ts, want, sent = [], [], []
vv = 0.0
for k in range(0, 46):
    tk = k * DT
    w = 1.6 if tk < 2.5 else 0.0
    ts.append(tk); want.append(w); sent.append(vv)
    if abs(w) > abs(vv):
        ch = max(-MA * DT, min(MA * DT, w - vv))
    else:
        ch = max(-MD * DT, min(MD * DT, w - vv))
    vv += ch
fig, ax = plt.subplots(figsize=(10, 5))
ax.step(ts, want, where="post", color=BLACK, ls="--", lw=2, label="wanted by the planner (a jump)")
ax.plot(ts, sent, "o-", color=BLUE, lw=2.5, ms=4, label="sent to the motors (limited)")
ax.text(0.6, 1.25, "slope 0.8 m/s^2\nreaches 1.6 m/s\nafter 2.0 s", fontsize=11.5, color=GREEN)
ax.text(3.45, 0.95, "slope -1.2 m/s^2\nstops after 1.33 s", fontsize=11.5, color=RED)
ax.set_xlabel("time t (s)"); ax.set_ylabel("velocity (m/s)"); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=11); ax.set_ylim(-0.1, 2.1)
save(fig, "fig03-ramp-limiter.png")

# Figure 4: accelerations from this chapter, in m/s^2 and in g
names = ["Rover\nspeeding up", "lift\nstarting", "Rover\nbraking", "gravity\n(1 g)", "landing,\nbent knees", "landing,\nstiff legs"]
vals = [0.8, 1.0, 1.2, 9.81, 10, 40]
cols = [BLUE, GREY, BLUE, BLACK, GREEN, RED]
fig, ax = plt.subplots(figsize=(11, 5))
ax.bar(range(len(vals)), vals, color=cols, edgecolor=BLACK)
ax.set_yscale("log"); ax.set_ylim(0.3, 100)
ax.set_yticks([0.5, 1, 2, 5, 10, 20, 50]); ax.set_yticklabels(["0.5", "1", "2", "5", "10", "20", "50"])
for i, val in enumerate(vals):
    ax.text(i, val * 1.12, f"{val:g} m/s^2\n= {val / 9.81:.2f} g", ha="center", fontsize=10.5)
ax.set_xticks(range(len(vals))); ax.set_xticklabels(names, fontsize=11)
ax.set_ylabel("acceleration (m/s^2), log scale"); ax.grid(axis="y", alpha=0.3)
save(fig, "fig04-accel-sizes.png")

# Figure 5: lift ride - accelerometer, velocity, height
random.seed(1)
D = 0.05


def ta(tk):
    return 1.0 if tk < 2 else (0.0 if tk < 8 else (-1.0 if tk < 10 else 0.0))


tl = [k * D for k in range(241)]
rd = [ta(tk) + random.gauss(0, 0.05) + 0.02 for tk in tl]
vel, h, ve, he = [], [], 0.0, 0.0
for r in rd:
    ve += r * D; he += ve * D; vel.append(ve); h.append(he)
tv = [min(tk, 2) * 1.0 - max(0, tk - 8) * 1.0 if tk < 10 else 0.0 for tk in tl]
th, hh = [], 0.0
for x in tv:
    hh += x * D; th.append(hh)
fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
axes[0].plot(tl, rd, color=GREY, lw=1, label="phone readings (noisy, +0.02 error)")
axes[0].plot(tl, [ta(tk) for tk in tl], color=BLACK, ls="--", lw=2, label="true acceleration")
axes[0].set_ylabel("a (m/s^2)"); axes[0].legend(loc="upper right", fontsize=10.5)
axes[1].plot(tl, vel, color=BLUE, lw=3, label="velocity from adding a x dt")
axes[1].plot(tl, tv, color=BLACK, ls="--", lw=2, label="true velocity")
axes[1].set_ylabel("v (m/s)"); axes[1].legend(loc="lower center", fontsize=10.5)
axes[2].plot(tl, h, color=BLUE, lw=3, label="height from adding v x dt")
axes[2].plot(tl, th, color=BLACK, ls="--", lw=2, label="true height")
axes[2].set_ylabel("height (m)"); axes[2].set_xlabel("time t (s)"); axes[2].legend(loc="upper left", fontsize=10.5)
for ax in axes:
    ax.grid(alpha=0.3)
save(fig, "fig05-lift-ride.png")

# Figure 6: a sharp start against a smooth start (jerk)
tj = np.linspace(0, 3, 600)
a_sharp = np.where(tj < 2, 0.8, 0.0)
ramp = np.clip(tj / 0.4, 0, 1) * np.clip((2.4 - tj) / 0.4, 0, 1)
a_smooth = 0.8 * ramp          # area 0.8 x 2.0 = 1.6 m/s, the same as the sharp start
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
axes[0].plot(tj, np.cumsum(a_sharp) * (tj[1] - tj[0]), color=RED, lw=3, label="sharp start")
axes[0].plot(tj, np.cumsum(a_smooth) * (tj[1] - tj[0]), color=GREEN, lw=3, label="smooth start")
axes[0].set_xlabel("time (s)"); axes[0].set_ylabel("velocity (m/s)"); axes[0].grid(alpha=0.3); axes[0].legend(loc="lower right")
axes[0].set_title("both reach 1.6 m/s", fontsize=12.5)
axes[1].plot(tj, a_sharp, color=RED, lw=3, label="sharp: acceleration jumps (huge jerk)")
axes[1].plot(tj, a_smooth, color=GREEN, lw=3, label="smooth: acceleration ramps (small jerk)")
axes[1].set_xlabel("time (s)"); axes[1].set_ylabel("acceleration (m/s^2)"); axes[1].grid(alpha=0.3)
axes[1].legend(loc="upper right", fontsize=10.5); axes[1].set_ylim(-0.05, 1.3)
axes[1].set_title("the jumps in acceleration are what jolt the load", fontsize=12.5)
save(fig, "fig06-jerk.png")
print("saved 6 figures")
