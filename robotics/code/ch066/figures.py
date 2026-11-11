# Figures for Chapter 66 - Moment of inertia.
# Run:  python figures.py      (saves PNG files in ../../images/ch066/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch066")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: the same 1 kg at different distances
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8), gridspec_kw={"width_ratios": [1.2, 1]})
ax = axes[0]
for k, (r, col) in enumerate([(0.1, GREEN), (0.2, BLUE), (0.4, RED)]):
    y = 2 - k
    ax.plot([0, 0.45], [y, y], color=GREY, lw=3)
    ax.plot([0], [y], "o", color=BLACK, ms=12)
    ax.plot([r], [y], "o", color=col, ms=20)
    ax.text(r, y + 0.25, f"1 kg at {r} m", ha="center", fontsize=11.5, color=col)
ax.text(-0.02, -0.55, "black dot: the axis it turns about", fontsize=11)
ax.set_xlim(-0.05, 0.5); ax.set_ylim(-0.8, 2.6); ax.axis("off")
ax = axes[1]
rs = [0.1, 0.2, 0.4]
ax.bar([str(r) + " m" for r in rs], [r ** 2 for r in rs], color=[GREEN, BLUE, RED], edgecolor=BLACK)
for i, r in enumerate(rs):
    ax.text(i, r ** 2 + 0.004, f"{r ** 2:.3f}", ha="center", fontsize=11.5)
ax.set_ylabel("moment of inertia I (kg m^2)"); ax.set_ylim(0, 0.185); ax.grid(axis="y", alpha=0.3)
ax.set_title("twice as far: four times as hard to spin", fontsize=12.5)
save(fig, "fig01-r-squared.png")

# Figure 2: common shapes
fig, axes = plt.subplots(1, 4, figsize=(15, 4))
ax = axes[0]
ax.plot([0, 1], [0, 0], color=ORANGE, lw=10); ax.plot([0], [0], "o", color=BLACK, ms=14)
ax.set_title("rod about its end\nI = M L^2 / 3", fontsize=12)
ax = axes[1]
ax.plot([-0.5, 0.5], [0, 0], color=ORANGE, lw=10); ax.plot([0], [0], "o", color=BLACK, ms=14)
ax.set_title("rod about its middle\nI = M L^2 / 12", fontsize=12)
ax = axes[2]
ax.add_patch(plt.Circle((0, 0), 0.45, color=ORANGE)); ax.plot([0], [0], "o", color=BLACK, ms=10)
ax.set_title("solid disc\nI = M R^2 / 2", fontsize=12)
ax = axes[3]
ax.add_patch(plt.Circle((0, 0), 0.45, fill=False, ec=ORANGE, lw=9)); ax.plot([0], [0], "o", color=BLACK, ms=10)
ax.set_title("thin ring\nI = M R^2", fontsize=12)
for ax in axes:
    ax.set_xlim(-0.6, 1.1); ax.set_ylim(-0.6, 0.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-shapes.png")

# Figure 3: 90 degree swing of the arm, angular speed against time
def profile(I, tmax=0.7, n=500):
    alpha = 3.0 / I
    wmax = 6.0
    ang = math.pi / 2
    ramp = wmax ** 2 / alpha
    if ang >= ramp:
        t1 = wmax / alpha; T = 2 * t1 + (ang - ramp) / wmax; peak = wmax
    else:
        t1 = math.sqrt(ang / alpha); T = 2 * t1; peak = alpha * t1
    t = np.linspace(0, tmax, n)
    w = np.clip(np.minimum.reduce([alpha * t, np.full_like(t, peak), alpha * (T - t)]), 0, None)
    return t, w, T


fig, ax = plt.subplots(figsize=(10, 5))
for (kg, at, col) in [(0.0, 0.5, GREY), (0.25, 0.5, BLUE), (0.5, 0.5, RED), (0.5, 0.25, GREEN)]:
    I = 0.4 * 0.25 / 3 + kg * at ** 2
    t, w, T = profile(I)
    ax.plot(t, w, color=col, lw=3, label=f"{kg} kg at {at} m: I = {I:.4f}, swing {T:.3f} s")
ax.axhline(6.0, color=BLACK, ls="--", lw=1.5); ax.text(0.005, 6.1, "speed limit 6 rad/s", fontsize=11)
ax.set_xlabel("time (s)"); ax.set_ylabel("joint speed omega (rad/s)"); ax.set_ylim(0, 7.5); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=10.5)
ax.set_title("each area under a curve is the same 90 deg (1.571 rad)", fontsize=12)
save(fig, "fig03-arm-swing.png")

# Figure 4: conservation of angular momentum - arms in, spin up
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, (arm, w, txt) in zip(axes, [(1.0, 2.0, "arms out: big I, omega = 2 rad/s"), (0.25, 6.0, "arms in: I three times smaller,\nomega = 6 rad/s")]):
    ax.add_patch(plt.Circle((0, 0), 0.25, color=ORANGE, ec=BLACK))
    ax.plot([-arm, arm], [0, 0], color=BLUE, lw=8, solid_capstyle="round")
    for s in (-1, 1):
        ax.plot([s * arm], [0], "o", color=RED, ms=16)
    t = np.linspace(0.3, 0.3 + 0.35 * w, 50)
    ax.plot(1.25 * np.cos(t), 1.25 * np.sin(t), color=BLACK, lw=1.5)
    ax.annotate("", xy=(1.25 * math.cos(t[-1]), 1.25 * math.sin(t[-1])), xytext=(1.25 * math.cos(t[-3]), 1.25 * math.sin(t[-3])),
                arrowprops=dict(arrowstyle="-|>", lw=1.5))
    ax.set_title(txt, fontsize=12)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_aspect("equal"); ax.axis("off")
fig.suptitle("angular momentum I x omega stays the same when nothing twists from outside", fontsize=12.5, y=1.06)
save(fig, "fig04-arms-in.png")

# Figure 5: reaction wheel - wheel speed and satellite angle
SAT_I, WHEEL_I, TQ = 20.0, 0.002, 0.01
a_sat = TQ / SAT_I
ang = math.pi / 2
T = 2 * math.sqrt(ang / a_sat)
t = np.linspace(0, T * 1.15, 500)
w_sat = np.where(t < T / 2, a_sat * t, np.where(t < T, a_sat * (T - t), 0))
theta = np.cumsum(w_sat) * (t[1] - t[0])
w_wheel = -SAT_I * w_sat / WHEEL_I
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
a1.plot(t, w_wheel * 60 / (2 * math.pi), color=RED, lw=3, label="reaction wheel speed (rpm)")
a1.set_ylabel("wheel (rpm)"); a1.grid(alpha=0.3); a1.legend(loc="lower right")
a2.plot(t, np.degrees(theta), color=BLUE, lw=3, label="satellite angle")
a2.axhline(90, color=BLACK, ls="--", lw=1.5); a2.text(2, 93, "target 90 deg", fontsize=11.5)
a2.set_ylabel("satellite (deg)"); a2.set_xlabel("time (s)"); a2.grid(alpha=0.3); a2.legend(loc="lower right")
a2.set_ylim(0, 105)
save(fig, "fig05-reaction-wheel.png")
print("saved 5 figures")
