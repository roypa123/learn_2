# Figures for Chapter 19 — Repeating part 1: while loops.
# Run:  python figures.py      (saves PNG files in ../../images/ch019/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch019")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


def rbox(ax, x, y, w, h, text, face, size=12, family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family)


def diamond(ax, cx, cy, w, h, text, size=12):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True,
                         fc=L_ORANGE, ec=BLACK, lw=1.3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=size, family=MONO)


def simulate(gain, dt=0.5, max_steps=50, start=1.0, sp=0.30, vmax=0.25, db=0.01):
    d, t, ts, ds, vs = start, 0.0, [0.0], [start], []
    e = d - sp
    n = 0
    while abs(e) >= db and n < max_steps:
        v = max(-vmax, min(vmax, gain * e))
        d -= v * dt
        t += dt
        n += 1
        e = d - sp
        ts.append(t); ds.append(d); vs.append(v)
    return ts, ds, vs


# ---------- Figure 1: the while flowchart ----------
fig, ax = plt.subplots(figsize=(12.5, 7.0))
rbox(ax, 3.6, 6.4, 4.0, 0.7, "count = 0", L_GREY, 13, MONO)
arrow(ax, (5.6, 6.38), (5.6, 5.75))
diamond(ax, 5.6, 4.75, 4.6, 2.0, "count < 3 ?", 14)
arrow(ax, (5.6, 3.75), (5.6, 3.1))
ax.text(5.8, 3.38, "True", fontsize=13, weight="bold", color=GREEN)
rbox(ax, 3.6, 1.8, 4.0, 1.25, "the BLOCK\nprint(count)\ncount += 1", L_GREEN, 12.5, MONO)
ax.plot([3.58, 1.5, 1.5], [2.42, 2.42, 4.75], color=BLUE, lw=3)
arrow(ax, (1.5, 4.75), (3.28, 4.75), BLUE, 3)
ax.text(1.35, 3.5, "go back and\nask AGAIN", ha="right", fontsize=12.5, color=BLUE, weight="bold")
arrow(ax, (7.9, 4.75), (9.4, 4.75))
ax.text(8.55, 4.95, "False", fontsize=13, weight="bold", color=RED, ha="center")
rbox(ax, 9.4, 4.25, 2.7, 1.0, "continue after\nthe loop", L_GREY, 12)
ax.text(5.6, 0.9, "An if asks once. A while asks every time round.", ha="center", fontsize=14, weight="bold")
ax.set_xlim(-0.6, 12.4); ax.set_ylim(0.5, 7.3); ax.axis("off")
save(fig, "fig01-while-flowchart.png")

# ---------- Figure 2: Rover driving to the wall ----------
ts, ds, vs = simulate(1.0)
fig, axes = plt.subplots(2, 1, figsize=(13, 7.0), sharex=True)
ax = axes[0]
ax.plot(ts, ds, "-o", color=BLUE, lw=2.2, label="distance to the wall")
ax.axhline(0.30, color=BLACK, ls="--", lw=2, label="setpoint 0.30 m")
ax.set_ylabel("distance (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper right")
ax.annotate("constant speed: the clamp is active", xy=(1.0, 0.75), xytext=(1.6, 0.92), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("stops here: within the deadband", xy=(ts[-1], ds[-1]), xytext=(3.0, 0.5), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax = axes[1]
ax.step(ts[1:], vs, where="post", color=GREEN, lw=2.5, label="speed command")
ax.set_xlabel("time (s)"); ax.set_ylabel("speed (m/s)"); ax.grid(alpha=0.3); ax.legend(loc="upper right")
ax.set_xlim(0, 5.2)
save(fig, "fig02-rover-drives-to-wall.png")

# ---------- Figure 3: changing the gain ----------
fig, ax = plt.subplots(figsize=(13, 5.4))
for g, c, st in [(0.5, GREY, "-"), (1.0, BLUE, "-"), (3.0, ORANGE, "-"), (4.0, RED, "-")]:
    ts, ds, _ = simulate(g, max_steps=24)
    ax.plot(ts, ds, st + "o", color=c, lw=2, ms=4, label=f"gain {g}  (gain x dt = {g * 0.5})")
ax.axhline(0.30, color=BLACK, ls="--", lw=2, label="setpoint 0.30 m")
ax.set_xlabel("time (s)"); ax.set_ylabel("distance (m)")
ax.set_xlim(0, 12); ax.grid(alpha=0.3); ax.legend(loc="upper right", framealpha=1)
ax.annotate("gain x dt = 2: it never settles;\nonly MAX_STEPS ends this loop", xy=(9, 0.25), xytext=(6.2, 0.55), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
save(fig, "fig03-changing-the-gain.png")

# ---------- Figure 4: stepping over a float target ----------
fig, ax = plt.subplots(figsize=(13, 3.8))
ax.plot([0.75, 1.25], [0, 0], color=BLACK, lw=1.5)
pts = [0.7999999999999999, 0.8999999999999999, 0.9999999999999999, 1.0999999999999999, 1.2]
for p in pts:
    ax.plot(p, 0, "o", color=BLUE, ms=10)
ax.plot([1.0, 1.0], [-0.35, 0.45], color=BLACK, ls="--", lw=2)
ax.text(1.0, 0.55, "the target: t != 1.0", ha="center", fontsize=13, weight="bold", family=MONO)
ax.annotate("0.9999999999999999\nnot equal to 1.0!", xy=(0.9999999999999999, 0), xytext=(0.82, 0.45), fontsize=12, color=BLUE,
            arrowprops=dict(arrowstyle="-|>", color=BLUE))
ax.annotate("next: 1.0999999999999999\nit has jumped past", xy=(1.0999999999999999, 0), xytext=(1.08, -0.65), fontsize=12, color=RED,
            arrowprops=dict(arrowstyle="-|>", color=RED))
ax.text(0.875, -0.6, "while t < 1.0 does end, but after 11 steps, not 10", fontsize=12, ha="center", color=GREEN, weight="bold")
ax.set_xlim(0.75, 1.25); ax.set_ylim(-0.95, 0.85); ax.axis("off")
save(fig, "fig04-float-steps-over-target.png")

# ---------- Figure 5: break and continue ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 5.4))
for ax, title, lines, target, tcol, note in [
    (axes[0], "continue: skip the rest, go to the top", ["while running:", "    read_sensor()", "    if bad_reading:", "        continue", "    drive()", "after_the_loop()"], 0, BLUE, "drive() is skipped this time"),
    (axes[1], "break: leave the loop now", ["while running:", "    read_sensor()", "    if e_stop:", "        break", "    drive()", "after_the_loop()"], 5, RED, "the loop is finished")]:
    ax.text(0.2, 6.5, title, fontsize=14, weight="bold")
    for i, t in enumerate(lines):
        ax.text(1.5, 5.5 - i * 0.82, t, family=MONO, fontsize=14, va="center", weight="bold" if i == 3 else "normal", color=tcol if i == 3 else BLACK)
    y0, y1 = 5.5 - 3 * 0.82, 5.5 - target * 0.82
    ax.plot([6.0, 7.1, 7.1], [y0, y0, y1], color=tcol, lw=3)
    arrow(ax, (7.1, y1), (6.3, y1), tcol, 3)
    ax.text(7.3, (y0 + y1) / 2, note, fontsize=12, color=tcol, va="center", weight="bold", rotation=90)
    ax.set_xlim(0, 8.2); ax.set_ylim(0.8, 7); ax.axis("off")
save(fig, "fig05-break-and-continue.png")
print("figures saved in", os.path.abspath(OUT))
