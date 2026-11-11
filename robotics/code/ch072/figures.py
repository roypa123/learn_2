# Figures for Chapter 72 - Project: a rolling cart on a ramp, measured and simulated.
# Run:  python figures.py      (saves PNG files in ../../images/ch072/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from ramp_data import FPS, RAMP_MARKS, FLAT_MARKS
from models import times_at_marks, CART_MASS_KG, C_RR, CD_A, RHO, SIN, COS, G, K

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch072")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: the set-up
fig, ax = plt.subplots(figsize=(11, 4.8))
th = math.asin(0.125)
Lr = 1.2
ax.fill([0, Lr * math.cos(th), 0], [Lr * math.sin(th), 0, 0], color=L_GREY)
ax.plot([0, Lr * math.cos(th)], [Lr * math.sin(th), 0], color=BLACK, lw=3)
ax.add_patch(plt.Rectangle((-0.08, 0), 0.08, Lr * math.sin(th), color=ORANGE, ec=BLACK))
ax.text(-0.04, 0.07, "books", rotation=90, ha="center", va="center", fontsize=10)
for k in range(0, 13):
    s = k * 0.1
    x, y = s * math.cos(th), Lr * math.sin(th) - s * math.sin(th)
    ax.plot([x, x + 0.02 * math.sin(th)], [y, y + 0.02 * math.cos(th)], color=RED, lw=2)
    if k % 2 == 0:
        ax.text(x + 0.005, y + 0.035, f"{s:.1f}", fontsize=9.5, color=RED, ha="center")
cx, cy = 0.05 * math.cos(th), Lr * math.sin(th) - 0.05 * math.sin(th)
ax.add_patch(plt.Polygon([(cx - 0.04, cy + 0.01), (cx + 0.04, cy), (cx + 0.04, cy + 0.04), (cx - 0.04, cy + 0.05)], color=BLUE, ec=BLACK))
ax.plot([Lr * math.cos(th), 1.9], [0, 0], color=BLACK, lw=2)
for k in range(0, 6):
    ax.plot([1.2 + k * 0.14, 1.2 + k * 0.14], [0, 0.02], color=GREEN, lw=2)
ax.text(1.5, 0.04, "flat marks every 0.2 m\n(coast-down test)", ha="center", fontsize=10.5, color=GREEN)
ax.add_patch(plt.Rectangle((0.5, -0.32), 0.12, 0.07, color=GREY, ec=BLACK)); ax.text(0.56, -0.38, "phone, filming from the side", ha="center", fontsize=10.5)
ax.text(0.65, 0.2, "ramp 1.20 m long, top 0.15 m higher; marks every 0.1 m", fontsize=11)
ax.set_xlim(-0.15, 1.95); ax.set_ylim(-0.45, 0.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-setup.png")

# Figure 2: the ramp measurements and the best s = 1/2 a t^2
t = np.array([f / FPS for s, f in RAMP_MARKS]); s = np.array([d for d, f in RAMP_MARKS])
a = 2 * np.sum(s * t ** 2) / np.sum(t ** 4)
tt = np.linspace(0, 1.7, 200)
fig, ax = plt.subplots(figsize=(10, 5))
ax.errorbar(t, s, xerr=0.5 / FPS, fmt="o", color=ORANGE, mec=BLACK, ms=8, capsize=3, label="video measurements (each +/- half a frame)")
ax.plot(tt, 0.5 * a * tt ** 2, color=BLUE, lw=2.5, label=f"best fit: s = 1/2 x {a:.3f} x t^2")
ax.set_xlabel("time since release (s)"); ax.set_ylabel("distance down the ramp (m)"); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=11)
save(fig, "fig02-ramp-fit.png")

# Figure 3: coast-down speeds
mid_t, sp = [], []
for (s0, f0), (s1, f1) in zip(FLAT_MARKS, FLAT_MARKS[1:]):
    mid_t.append((f0 + f1) / 2 / FPS); sp.append((s1 - s0) / ((f1 - f0) / FPS))
mid_t, sp = np.array(mid_t), np.array(sp)
slope = np.sum((mid_t - mid_t.mean()) * (sp - sp.mean())) / np.sum((mid_t - mid_t.mean()) ** 2)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(mid_t, sp, "s", color=GREEN, mec=BLACK, ms=9, label="average speed between two marks")
tl = np.linspace(0, 2.7, 50)
ax.plot(tl, sp.mean() + slope * (tl - mid_t.mean()), color=BLUE, lw=2.5, label=f"best straight line: slope {slope:.3f} m/s^2")
ax.set_xlabel("time (s)"); ax.set_ylabel("speed on the flat (m/s)"); ax.set_ylim(0.3, 1.15); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=11)
ax.set_title("the points jump because each time is rounded to a whole video frame", fontsize=12)
save(fig, "fig03-coast-down.png")

# Figure 4: the four models against the measurements
meas = [f / FPS for d, f in RAMP_MARKS]
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.plot(meas, s, "o", color=ORANGE, mec=BLACK, ms=9, label="measured", zorder=5)
for (name, w, r, d), col, ls in zip([("1: sliding only", False, False, False), ("2: + spinning wheels", True, False, False),
                                     ("3: + rolling resistance", True, True, False), ("4: + air drag", True, True, True)],
                                    [RED, GREY, BLUE, GREEN], ["-", "-", "-", "--"]):
    sim, ve = times_at_marks(w, r, d)
    ax.plot(sim, s, ls, color=col, lw=2.5, label=f"model {name}")
ax.set_xlabel("time (s)"); ax.set_ylabel("distance down the ramp (m)"); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("models 1 and 2 arrive too early; models 3 and 4 match the video", fontsize=12.5)
save(fig, "fig04-models.png")

# Figure 5: RMS error of each model, in video frames
names = ["1: sliding\nonly", "2: + spinning\nwheels", "3: + rolling\nresistance", "4: + air\ndrag"]
rms = []
for w, r, d in [(False, False, False), (True, False, False), (True, True, False), (True, True, True)]:
    sim, ve = times_at_marks(w, r, d)
    rms.append(math.sqrt(sum((x - y) ** 2 for x, y in zip(sim, meas)) / len(sim)) * FPS)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.bar(range(4), rms, color=[RED, GREY, BLUE, GREEN], edgecolor=BLACK)
for i, r in enumerate(rms):
    ax.text(i, r + 0.08, f"{r:.2f}", ha="center", fontsize=11.5)
ax.axhline(0.29, color=BLACK, ls="--", lw=1.5); ax.text(1.5, 0.9, "dashed line: the error from rounding to whole frames alone (0.29)", ha="center", fontsize=10.5)
ax.set_xticks(range(4)); ax.set_xticklabels(names); ax.set_ylabel("RMS error (video frames)"); ax.grid(axis="y", alpha=0.3)
ax.set_ylim(0, 5)
save(fig, "fig05-rms.png")

# Figure 6: the forces on the cart along the ramp at 1.5 m/s
grav = CART_MASS_KG * G * SIN
roll = C_RR * CART_MASS_KG * G * COS
drag = 0.5 * RHO * CD_A * 1.5 ** 2
fig, ax = plt.subplots(figsize=(10, 4.5))
vals = [grav, roll, drag]
labels = ["gravity along\nthe ramp", "rolling\nresistance", "air drag\nat 1.5 m/s"]
ax.barh(range(3), vals, color=[BLUE, RED, GREEN], edgecolor=BLACK)
for i, v in enumerate(vals):
    ax.text(v + 0.005, i, f"{v * 1000:.1f} mN  ({v / grav:.1%} of gravity's pull)", va="center", fontsize=11.5)
ax.set_yticks(range(3)); ax.set_yticklabels(labels); ax.invert_yaxis(); ax.set_xlim(0, 0.56)
ax.set_xlabel("force along the ramp (N)"); ax.grid(axis="x", alpha=0.3)
save(fig, "fig06-force-budget.png")
print("saved 6 figures")
