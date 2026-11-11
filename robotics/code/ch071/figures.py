# Figures for Chapter 71 - Simulating physics in Python: Euler's method.
# Run:  python figures.py      (saves PNG files in ../../images/ch071/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch071")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
G = 9.81


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: Euler steps against the true curve for a falling ball
t = np.linspace(0, 2, 300)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(t, 0.5 * G * t ** 2, color=BLACK, ls="--", lw=2, label="exact: 1/2 g t^2")
for dt, col in [(0.5, RED), (0.1, BLUE)]:
    ts, xs, x, v = [0.0], [0.0], 0.0, 0.0
    for k in range(round(2 / dt)):
        x = x + v * dt; v = v + G * dt
        ts.append((k + 1) * dt); xs.append(x)
    ax.plot(ts, xs, "o-", color=col, lw=2, ms=7, label=f"Euler, dt = {dt} s")
ax.set_xlabel("time (s)"); ax.set_ylabel("distance fallen (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
ax.set_title("each step goes straight, using the speed at the start of the step", fontsize=12.5)
save(fig, "fig01-euler-steps.png")

# Figure 2: error against step size (log scales)
dts = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
errs = []
for dt in dts:
    x = v = 0.0
    for k in range(round(2 / dt)):
        x = x + v * dt; v = v + G * dt
    errs.append(abs(x - 0.5 * G * 4))
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(dts, errs, "o-", color=BLUE, lw=2.5, ms=8)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xticks([0.001, 0.01, 0.1, 1]); ax.set_xticklabels(["0.001", "0.01", "0.1", "1"])
ax.set_yticks([0.01, 0.1, 1, 10]); ax.set_yticklabels(["0.01", "0.1", "1", "10"])
ax.set_xlabel("time step dt (s), log scale"); ax.set_ylabel("error after 2 s (m), log scale"); ax.grid(alpha=0.3, which="both")
ax.set_title("ten times smaller steps, ten times smaller error", fontsize=12.5)
save(fig, "fig02-error-vs-dt.png")

# Figure 3: falling drone with and without parachute
def fall(open_at):
    tt, hh, vv = [0.0], [30.0], [0.0]
    t_, h, v = 0.0, 30.0, 0.0
    while h > 0:
        cda = 1.2 if t_ >= open_at else 0.05
        a = (1.6 * G - 0.5 * 1.2 * cda * v * v) / 1.6
        h -= v * 0.001; v += a * 0.001; t_ += 0.001
        tt.append(t_); hh.append(h); vv.append(v)
    return np.array(tt), np.array(hh), np.array(vv)


fig, ax = plt.subplots(figsize=(10, 5))
t0, h0, v0 = fall(99)
t1, h1, v1 = fall(1.5)
tv = np.linspace(0, 2.5, 100)
ax.plot(tv, G * tv, color=GREY, ls=":", lw=2, label="no air at all: v = g t")
ax.plot(t0, v0, color=RED, lw=3, label=f"with drag, no parachute: lands at {v0[-1]:.1f} m/s")
ax.plot(t1, v1, color=BLUE, lw=3, label=f"parachute opens at 1.5 s: lands at {v1[-1]:.2f} m/s")
ax.axhline(22.87, color=RED, ls="--", lw=1); ax.text(3.3, 23.4, "terminal speed 22.9 m/s", fontsize=11, color=RED)
ax.axhline(4.67, color=BLUE, ls="--", lw=1); ax.text(3.3, 5.2, "terminal speed 4.67 m/s", fontsize=11, color=BLUE)
ax.set_xlabel("time since the motors stopped (s)"); ax.set_ylabel("falling speed (m/s)"); ax.set_ylim(0, 26); ax.set_xlim(0, 5.6)
ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10.5, bbox_to_anchor=(1.0, 0.85))
save(fig, "fig03-drag-fall.png")

# Figure 4: spring - plain Euler against semi-implicit Euler
K, M, DT = 40.0, 1.0, 0.02
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, method, col in [(axes[0], "plain Euler", RED), (axes[1], "semi-implicit Euler", BLUE)]:
    x, v = 0.1, 0.0
    xs, vs = [x], [v]
    for k in range(500):
        a = -K * x / M
        if method == "plain Euler":
            x, v = x + v * DT, v + a * DT
        else:
            v = v + a * DT; x = x + v * DT
        xs.append(x); vs.append(v)
    ax.plot(xs, vs, color=col, lw=1.2)
    ax.plot([0.1], [0.0], "o", color=BLACK, ms=8)
    ax.set_xlabel("position x (m)"); ax.set_ylabel("velocity v (m/s)"); ax.grid(alpha=0.3)
    ax.set_title(f"{method}: 10 s, 500 steps", fontsize=12.5)
axes[1].set_xticks([-0.1, -0.05, 0.0, 0.05, 0.1])
axes[0].text(0.03, 0.95, "spirals outwards:\nenergy grows from nothing", transform=axes[0].transAxes, fontsize=11.5, va="top", color=RED)
axes[1].text(0.03, 0.95, "stays on its loop:\nenergy stays steady", transform=axes[1].transAxes, fontsize=11.5, va="top", color=BLUE)
save(fig, "fig04-spring-euler.png")

# Figure 5: Rover speeding up with a real motor
WR, N, S, F, E = 0.033, 30, 0.010, 12000 * 2 * math.pi / 60, 0.8
R = 0.015 * 4 * G
me = 5.65


def push(v):
    return 2 * S * max(0.0, 1 - v / WR * N / F) * N * E / WR


ts, vs, t_, v = [0.0], [0.0], 0.0, 0.0
while t_ < 3.0:
    v += (push(v) - R) / me * 0.001; t_ += 0.001
    ts.append(t_); vs.append(v)
vtop = F * WR / N * (1 - R / push(0))
a0 = (push(0) - R) / me
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(ts, vs, color=BLUE, lw=3, label="Euler simulation with the real motor")
tl = np.linspace(0, 0.6, 50)
ax.plot(tl, a0 * tl, color=RED, ls="--", lw=2, label=f"if the starting acceleration {a0:.2f} m/s^2 lasted")
ax.axhline(vtop, color=BLACK, ls=":", lw=1.5); ax.text(2.0, vtop + 0.04, f"top speed {vtop:.3f} m/s", fontsize=11.5)
ax.axhline(0.95 * vtop, color=GREY, ls=":", lw=1); ax.plot([1.608], [0.95 * vtop], "o", color=BLUE, ms=8)
ax.text(1.65, 0.95 * vtop - 0.13, "95% after 1.61 s", fontsize=11.5)
ax.set_xlabel("time (s)"); ax.set_ylabel("Rover's speed (m/s)"); ax.set_ylim(0, 1.6); ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=11)
save(fig, "fig05-rover-speedup.png")
print("saved 5 figures")
