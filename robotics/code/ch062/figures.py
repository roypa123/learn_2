# Figures for Chapter 62 - Mass, weight and gravity.
# Run:  python figures.py      (saves PNG files in ../../images/ch062/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch062")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
G = 9.81


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: mass and weight of Rover on three worlds
names = ["Earth", "Moon", "Mars"]
gs = [9.81, 1.62, 3.71]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
axes[0].bar(names, [4.0] * 3, color=[BLUE, GREY, RED], edgecolor=BLACK)
axes[0].set_ylabel("mass (kg)"); axes[0].set_ylim(0, 5); axes[0].set_title("mass: the same everywhere", fontsize=12.5)
for i in range(3):
    axes[0].text(i, 4.1, "4.0 kg", ha="center", fontsize=11.5)
w = [4.0 * g for g in gs]
axes[1].bar(names, w, color=[BLUE, GREY, RED], edgecolor=BLACK)
axes[1].set_ylabel("weight (N)"); axes[1].set_ylim(0, 45); axes[1].set_title("weight = mass x g: changes with the world", fontsize=12.5)
for i, v in enumerate(w):
    axes[1].text(i, v + 0.8, f"{v:.2f} N\n(g = {gs[i]})", ha="center", fontsize=11)
for ax in axes:
    ax.grid(axis="y", alpha=0.3)
save(fig, "fig01-mass-weight.png")

# Figure 2: g against height above the Earth
GM = 6.674e-11 * 5.972e24
R = 6.371e6
h = np.linspace(0, 40000, 400)
g = GM / (R + h * 1000) ** 2
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(h, g, color=BLUE, lw=3)
for hk, lab in [(0, "ground"), (400, "space station, 400 km"), (36000, "TV satellites, 36,000 km")]:
    gk = GM / (R + hk * 1000) ** 2
    ax.plot([hk], [gk], "o", color=RED, ms=9)
    ax.text(hk + 700, gk + 0.35, f"{lab}: {gk:.2f}", fontsize=11.5)
ax.set_xlabel("height above the ground (km)"); ax.set_ylabel("g (m/s^2)"); ax.set_ylim(0, 11); ax.grid(alpha=0.3)
ax.set_title("gravity gets weaker with distance, but slowly at first", fontsize=12.5)
save(fig, "fig02-g-height.png")

# Figure 3: the scale reading in a lift
t = np.linspace(0, 12, 600)
a = np.where(t < 2, 1.0, np.where(t < 8, 0.0, np.where(t < 10, -1.0, 0.0)))
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, 30 * (G + a), color=BLUE, lw=3, label="scale reading under a 30 kg robot")
ax.axhline(30 * G, color=BLACK, ls="--", lw=1.5, label="true weight 294.3 N")
ax.text(1.0, 330, "speeding up:\nreads more", ha="center", fontsize=11.5)
ax.text(9.0, 240, "slowing down:\nreads less", ha="center", fontsize=11.5)
ax.set_xlabel("time (s)"); ax.set_ylabel("force on the scale (N)"); ax.set_ylim(220, 360); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=11)
ax.set_title("a lift going up", fontsize=12.5)
save(fig, "fig03-lift-scale.png")

# Figure 4: a tilted accelerometer
p = math.radians(20)
fig, ax = plt.subplots(figsize=(8, 7))
ax.fill_between([-3, 3], -3.2, -2.8, color=L_GREY)
c, s = math.cos(p), math.sin(p)
box = [(-1.2, -0.4), (1.2, -0.4), (1.2, 0.4), (-1.2, 0.4)]
ax.add_patch(plt.Polygon([(c * x - s * y, s * x + c * y) for x, y in box], color=ORANGE, ec=BLACK, alpha=0.8))


def arr(x1, y1, col, lw=3, x0=0.0, y0=0.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=20))


arr(2.2 * c, 2.2 * s, GREY, 2); ax.text(2.25 * c, 2.25 * s - 0.25, "x axis\n(forwards)", fontsize=11)
arr(-2.6 * s, 2.6 * c, GREY, 2); ax.text(-2.6 * s - 1.0, 2.6 * c, "z axis\n(robot's up)", fontsize=11)
arr(0, 2.6, BLUE, 3.5); ax.text(0.1, 2.7, "reading: 9.81 m/s^2 straight up", fontsize=12, color=BLUE)
ax.plot([0, 2.6 * s * c], [2.6, 2.6 * s * s], color=GREY, ls=":", lw=1.5)
arr(2.6 * s * c, 2.6 * s * s, RED, 2.5); ax.text(2.6 * s * c + 0.25, 2.6 * s * s - 0.75, "ax = 9.81 sin(pitch)", fontsize=11.5, color=RED)
arr(-2.6 * c * s, 2.6 * c * c, GREEN, 2.5); ax.text(-2.6 * c * s - 2.2, 2.6 * c * c - 0.4, "az = 9.81 cos(pitch)", fontsize=11.5, color=GREEN)
tt = np.linspace(math.pi / 2, math.pi / 2 + p, 20)
ax.plot(1.2 * np.cos(tt), 1.2 * np.sin(tt), color=BLACK, lw=1.2)
ax.text(-0.45, 1.3, "pitch", fontsize=11)
arr(0, -2.4, BLACK, 2); ax.text(0.1, -2.3, "gravity pulls down", fontsize=11)
ax.set_xlim(-3.2, 3.6); ax.set_ylim(-3.2, 3.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-tilted-accel.png")

# Figure 5: tilt estimates with noise
random.seed(3)


def reading(pd, noise):
    q = math.radians(pd)
    return G * math.sin(q) + random.gauss(0, noise), G * math.cos(q) + random.gauss(0, noise)


fig, ax = plt.subplots(figsize=(10, 4.8))
for k in range(5):
    reading(15, 0.2)
est = [math.degrees(math.atan2(*reading(15, 0.2))) for k in range(100)]
ax.plot(range(1, 101), est, ".", color=GREY, ms=8, label="one reading each")
run = np.cumsum(est) / np.arange(1, 101)
ax.plot(range(1, 101), run, color=BLUE, lw=3, label="average of all readings so far")
ax.axhline(15, color=BLACK, ls="--", lw=2, label="true pitch 15 deg")
ax.set_xlabel("reading number"); ax.set_ylabel("pitch estimate (deg)"); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=10.5); ax.set_ylim(11, 20.5)
save(fig, "fig05-tilt-noise.png")
print("saved 5 figures")
