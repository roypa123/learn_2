# Figures for Chapter 59 - Equations of motion with constant acceleration.
# Run:  python figures.py      (saves PNG files in ../../images/ch059/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch059")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: the area under a straight velocity line, split into a rectangle and a triangle
u, a, T = 0.4, 0.5, 4.0
v = u + a * T
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.fill_between([0, T], [0, 0], [u, u], color=L_BLUE)
ax.fill_between([0, T], [u, u], [u, v], color=L_GREEN)
ax.plot([0, T], [u, v], color=BLUE, lw=3)
ax.text(2, 0.2, "rectangle: u x t = 0.4 x 4 = 1.6 m", ha="center", fontsize=12)
ax.text(2.75, 0.85, "triangle: 1/2 x t x (a t)\n= 1/2 x 4 x 2.0 = 4.0 m", ha="center", fontsize=12)
ax.annotate("", xy=(T + 0.15, v), xytext=(T + 0.15, u), arrowprops=dict(arrowstyle="<->", lw=1.5))
ax.text(T + 0.25, 1.95, "a t = 2.0 m/s", fontsize=12, va="center")
ax.annotate("", xy=(T + 0.15, u), xytext=(T + 0.15, 0), arrowprops=dict(arrowstyle="<->", lw=1.5))
ax.text(T + 0.25, u / 2, "u = 0.4 m/s", fontsize=12, va="center")
ax.plot([0, T], [(u + v) / 2] * 2, color=RED, ls="--", lw=2)
ax.text(T + 0.25, 1.25, "average velocity\n(u + v) / 2\n= 1.4 m/s", fontsize=11.5, color=RED, va="center")
ax.text(0.1, 2.25, "total area = 1.6 + 4.0 = 5.6 m = displacement s", fontsize=12.5)
ax.set_xlim(0, 5.7); ax.set_ylim(0, 2.6)
ax.set_xlabel("time t (s)"); ax.set_ylabel("velocity (m/s)"); ax.grid(alpha=0.3)
save(fig, "fig01-trapezium.png")

# Figure 2: position under constant acceleration is a parabola
t = np.linspace(0, 4, 200)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, 0.5 * 1.0 * t ** 2, color=BLUE, lw=3, label="from rest, a = 1.0 m/s^2: s = 0.5 t^2")
ax.plot(t, 1.0 * t, color=GREY, lw=2.5, ls="--", label="steady 1.0 m/s, no acceleration: s = t")
for tk in [1, 2, 3, 4]:
    ax.plot([tk], [0.5 * tk ** 2], "o", color=BLUE, ms=8)
    ax.text(tk - 0.05, 0.5 * tk ** 2 + 0.35, f"{0.5 * tk ** 2:g} m", ha="right", fontsize=11.5)
ax.text(2.3, 1.0, "double the time -> four times the distance\n(1 s: 0.5 m, 2 s: 2 m, 4 s: 8 m)", fontsize=11.5)
ax.set_ylim(-0.3, 9.0); ax.set_xlabel("time t (s)"); ax.set_ylabel("displacement s (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig02-parabola.png")

# Figure 3: stopping distance = reaction + braking
vs = np.linspace(0, 3, 200)
re = vs * 0.3
br = vs ** 2 / 3.0
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.fill_between(vs, 0, re, color=L_ORANGE, label="reaction distance v x 0.3 (straight line)")
ax.fill_between(vs, re, re + br, color=L_BLUE, label="braking distance v^2 / (2 x 1.5) (parabola)")
ax.plot(vs, re + br, color=BLUE, lw=3, label="total stopping distance")
ax.axhline(2.0, color=RED, ls="--", lw=2)
ax.text(0.05, 2.08, "free space the sensor can see: 2.0 m", color=RED, fontsize=12)
ax.plot([2.0405], [2.0], "o", color=RED, ms=10)
ax.annotate("fastest safe speed\n2.04 m/s", (2.0405, 2.0), xytext=(2.25, 0.9), fontsize=12,
            arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("speed v (m/s)"); ax.set_ylabel("distance (m)"); ax.set_xlim(0, 3); ax.set_ylim(0, 4)
ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig03-stopping.png")

# Figure 4: trapezoid and triangle move profiles
def profile(D, vmax, acc, n=400):
    ramp = vmax ** 2 / acc
    if D >= ramp:
        t1 = vmax / acc; tc = (D - ramp) / vmax; T = 2 * t1 + tc; vp = vmax
    else:
        vp = math.sqrt(acc * D); t1 = vp / acc; tc = 0.0; T = 2 * t1
    tt = np.linspace(0, T, n)
    vv = np.minimum.reduce([acc * tt, np.full_like(tt, vp), acc * (T - tt)])
    return tt, vv, T


fig, ax = plt.subplots(figsize=(10, 5.2))
for vmax, col, ls in [(1.5, BLUE, "-"), (3.0, RED, "--")]:
    tt, vv, T = profile(0.6, vmax, 6.0)
    ax.plot(tt, vv, color=col, lw=3, ls=ls, label=f"top speed allowed {vmax} m/s: move takes {T:.3f} s")
ax.axhline(1.5, color=GREY, lw=1, ls=":")
ax.axhline(3.0, color=GREY, lw=1, ls=":")
ax.text(0.33, 1.58, "trapezoid: reaches 1.5 m/s, cruises, slows", fontsize=11.5, color=BLUE)
ax.text(0.33, 2.0, "triangle: peaks at 1.90 m/s,\nnever reaches 3.0 m/s", fontsize=11.5, color=RED)
ax.set_xlabel("time t (s)"); ax.set_ylabel("velocity (m/s)"); ax.set_ylim(0, 3.3); ax.set_xlim(0, 0.75)
ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=11)
ax.set_title("one 0.6 m move of the arm, acceleration 6 m/s^2 (area under each line = 0.6 m)", fontsize=12)
save(fig, "fig04-move-profiles.png")

# Figure 5: falling - the ruler drop table of Chapter 6
tt = np.linspace(0, 0.27, 200)
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(tt, 100 * 0.5 * 9.81 * tt ** 2, color=BLUE, lw=3, label="s = 1/2 g t^2 (in cm)")
for d in [5, 10, 15, 20, 30]:
    tk = math.sqrt(2 * d / 100 / 9.81)
    ax.plot([tk], [d], "o", color=RED, ms=8)
    ax.plot([tk, tk], [0, d], color=GREY, ls=":", lw=1.2)
    ax.text(tk - 0.004, d + 1.2, f"{d} cm: {tk:.3f} s", ha="right", fontsize=11)
ax.set_xlabel("time since the ruler was let go (s)"); ax.set_ylabel("distance fallen (cm)")
ax.set_xlim(0, 0.27); ax.set_ylim(0, 37); ax.grid(alpha=0.3); ax.legend(loc="upper left")
save(fig, "fig05-ruler-drop.png")

# Figure 6: a cart rolling down a ramp - s against t and s against t^2
tm = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
sm = np.array([0.0, 0.05, 0.21, 0.46, 0.81])
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
axes[0].plot(tm, sm, "o", color=ORANGE, mec=BLACK, ms=10, label="measured")
tf = np.linspace(0, 2, 100)
axes[0].plot(tf, 0.2025 * tf ** 2, color=BLUE, lw=2.5, label="s = 0.2025 t^2")
axes[0].set_xlabel("time t (s)"); axes[0].set_ylabel("distance down the ramp s (m)")
axes[0].set_title("against t: a curve", fontsize=12.5)
axes[1].plot(tm ** 2, sm, "o", color=ORANGE, mec=BLACK, ms=10, label="measured")
axes[1].plot([0, 4], [0, 0.81], color=BLUE, lw=2.5, label="straight line, slope 0.2025 = a / 2")
axes[1].set_xlabel("time squared t^2 (s^2)"); axes[1].set_ylabel("distance down the ramp s (m)")
axes[1].set_title("against t^2: a straight line", fontsize=12.5)
for ax in axes:
    ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig06-ramp-cart.png")
print("saved 6 figures")
