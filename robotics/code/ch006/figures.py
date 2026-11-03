# Figures for Chapter 6 — How a robot "thinks": the control loop.
# Run:  python figures.py      (saves PNG files in ../../images/ch006/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch006")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
PURPLE, SKY = "#CC79A7", "#56B4E9"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=2.0, rad=0.0, label=None, lpos=None, lcol=BLACK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))
    if label:
        x, y = lpos if lpos else ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.2)
        ax.text(x, y, label, ha="center", fontsize=11, color=lcol, style="italic")


# ---------- Figure 1: catching a ball as a loop ----------
fig, ax = plt.subplots(figsize=(12, 6))
box(ax, 0.0, 3.2, 2.8, 1.3, "EYES\nwhere is the ball?\nwhere is my hand?", L_BLUE)
box(ax, 4.2, 3.2, 3.2, 1.3, "BRAIN\nwhere will it land?\nhow far is my hand?", L_ORANGE)
box(ax, 8.8, 3.2, 2.8, 1.3, "ARM MUSCLES\nmove the hand\ntowards the ball", L_GREEN)
box(ax, 4.2, 0.2, 3.2, 1.2, "HAND + BALL\n(the world changes)", L_GREY)
arrow(ax, (2.8, 3.85), (4.2, 3.85), label="measure")
arrow(ax, (7.4, 3.85), (8.8, 3.85), label="command")
arrow(ax, (10.2, 3.2), (7.4, 0.8), rad=-0.2)
arrow(ax, (4.2, 0.8), (1.4, 3.2), rad=-0.2)
ax.text(10.0, 1.6, "correct", fontsize=11, style="italic"); ax.text(1.2, 1.6, "look again", fontsize=11, style="italic")
ax.text(5.8, 5.0, "about 10 times per second, until the ball is caught", ha="center", fontsize=12.5, color=BLUE, weight="bold")
ax.set_xlim(-0.3, 11.9); ax.set_ylim(-0.1, 5.4); ax.axis("off")
save(fig, "fig01-catching-loop.png")

# ---------- Figure 2: the general control loop with its names ----------
fig, ax = plt.subplots(figsize=(14, 6.2))
ax.text(0.0, 3.55, "SETPOINT\n(what we want)", ha="left", va="center", fontsize=12, weight="bold")
ax.add_patch(Circle((3.0, 3.55), 0.35, fc="white", ec=BLACK, lw=1.5))
ax.text(2.45, 3.95, "+", fontsize=14); ax.text(2.6, 2.85, "−", fontsize=16)
ax.text(3.0, 4.15, "compare", ha="center", fontsize=10.5, style="italic")
arrow(ax, (1.9, 3.55), (2.65, 3.55), BLACK)
arrow(ax, (3.35, 3.55), (4.6, 3.55), RED, label="ERROR", lpos=(3.95, 3.8), lcol=RED)
box(ax, 4.6, 3.0, 2.4, 1.1, "CONTROLLER\n(the rule)", L_ORANGE)
arrow(ax, (7.0, 3.55), (8.2, 3.55), GREEN, label="COMMAND", lpos=(7.6, 3.8), lcol=GREEN)
box(ax, 8.2, 3.0, 2.0, 1.1, "ACTUATOR\n(motor)", L_GREEN)
arrow(ax, (10.2, 3.55), (11.2, 3.55), GREY)
box(ax, 11.2, 3.0, 2.2, 1.1, "SYSTEM\n(the robot\nin the world)", L_GREY)
ax.text(12.3, 5.35, "DISTURBANCE\n(wind, a bump, a slope)", ha="center", fontsize=11, color=PURPLE)
arrow(ax, (12.3, 4.95), (12.3, 4.1), PURPLE)
arrow(ax, (13.4, 3.55), (14.3, 3.55), BLUE, label="OUTPUT", lpos=(13.95, 3.8), lcol=BLUE)
ax.plot([13.9, 13.9], [3.55, 1.0], color=BLUE, lw=2)
box(ax, 7.6, 0.45, 2.4, 1.1, "SENSOR", L_BLUE)
arrow(ax, (13.9, 1.0), (10.0, 1.0), BLUE)
ax.plot([7.6, 3.0], [1.0, 1.0], color=BLUE, lw=2)
arrow(ax, (3.0, 1.0), (3.0, 3.2), BLUE, label="MEASUREMENT", lpos=(4.6, 1.25), lcol=BLUE)
ax.text(7.0, -0.35, "error = setpoint − measurement", ha="center", fontsize=13, color=RED, weight="bold")
ax.set_xlim(-0.2, 14.6); ax.set_ylim(-0.7, 6.0); ax.axis("off")
save(fig, "fig02-control-loop-names.png")

# ---------- simulation helpers ----------
def hand_run(gain, steps=21, dt=0.05, setpoint=1.2, delay=0, target=None):
    hands, h = [], 0.0
    for s in range(steps):
        hands.append(h)
        seen = hands[max(0, s - delay)]                 # what the eye reports (maybe old)
        sp = setpoint if target is None else target(s * dt)
        h = h + gain * (sp - seen) * dt
    return [s * dt for s in range(steps)], hands

# ---------- Figure 3: four gains ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axhline(1.2, color=BLACK, ls="--", lw=2, label="setpoint: ball lands at 1.2 m")
for gain, colour, ls in [(1, GREY, ":"), (4, BLUE, "-"), (30, ORANGE, "--"), (45, RED, "-.")]:
    t, h = hand_run(gain)
    if gain == 45:
        t, h = t[:4], h[:4]          # it runs away fast: show only the first loops
    ax.plot(t, h, color=colour, ls=ls, lw=2.5, marker="o", ms=4, label=f"gain {gain}")
ax.axvspan(0.95, 1.05, color=GREEN, alpha=0.15); ax.text(0.86, 1.9, "ball\narrives", fontsize=11, color=GREEN)
ax.set_xlabel("time (seconds)"); ax.set_ylabel("hand position (metres)")
ax.set_ylim(-0.6, 3.0); ax.grid(alpha=0.3); ax.legend(loc="lower right", fontsize=11)
ax.annotate("gain 45: each correction is too big; the hand swings\nfurther and further (off the picture after 0.15 s)",
            xy=(0.15, 2.4), xytext=(0.22, 2.55), fontsize=10.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED))
save(fig, "fig03-four-gains.png")

# ---------- Figure 4: delay ----------
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.axhline(1.2, color=BLACK, ls="--", lw=2, label="setpoint")
for gain, delay, colour, ls, lab in [(4, 0, BLUE, "-", "gain 4, no delay"),
                                     (4, 4, ORANGE, "--", "gain 4, eyes 0.2 s late"),
                                     (8, 4, RED, "-.", "gain 8, eyes 0.2 s late")]:
    t, h = hand_run(gain, steps=41, delay=delay)
    ax.plot(t, h, color=colour, ls=ls, lw=2.5, label=lab)
ax.set_xlabel("time (seconds)"); ax.set_ylabel("hand position (metres)")
ax.set_ylim(-0.2, 2.3); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=11)
save(fig, "fig04-delay.png")

# ---------- Figure 5: Rover at the wall, on-off (Ch 2) vs proportional ----------
def on_off():
    d, out = 1.0, []
    while True:
        out.append(d)
        if d > 0.3: d -= 0.25 * 0.5
        else: break
    return out
def proportional():
    d, out = 1.0, []
    for _ in range(13):
        out.append(d)
        d -= max(0.0, min(0.25, 1.0 * (d - 0.3))) * 0.5
    return out
a, b = on_off(), proportional()
fig, axs = plt.subplots(1, 2, figsize=(13, 5))
ax = axs[0]
ax.axhline(0.3, color=BLACK, ls="--", lw=2, label="setpoint 0.3 m")
ax.plot(range(len(a)), a, "s:", color=GREY, lw=2.5, ms=7, label="on-off (Chapter 2)")
ax.plot(range(len(b)), b, "o-", color=BLUE, lw=2.5, ms=7, label="proportional (this chapter)")
ax.set_xlabel("loop number (one loop = 0.5 s)"); ax.set_ylabel("distance to the wall (m)")
ax.set_ylim(0.2, 1.05); ax.grid(alpha=0.3); ax.legend()
ax.set_title("distance")
ax = axs[1]
sa = [0.25 if d > 0.3 else 0 for d in a]
sb = [max(0.0, min(0.25, d - 0.3)) for d in b]
ax.step(range(len(sa)), sa, where="post", color=GREY, ls=":", lw=2.5, label="on-off: full speed, then stop")
ax.plot(range(len(sb)), sb, "o-", color=GREEN, lw=2.5, label="proportional: slows down near the wall")
ax.set_xlabel("loop number"); ax.set_ylabel("speed command (m/s)"); ax.set_title("speed command")
ax.set_ylim(-0.02, 0.3); ax.grid(alpha=0.3); ax.legend(loc="lower left")
fig.tight_layout()
save(fig, "fig05-wall-onoff-vs-proportional.png")

# ---------- Figure 6: following a person ----------
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.axhline(1.0, color=BLACK, ls="--", lw=2, label="setpoint: 1.0 m behind")
for gain, colour, ls in [(2, ORANGE, "--"), (5, BLUE, "-")]:
    person, robot, ts, gaps = 1.0, 0.0, [], []
    for step in range(101):
        gap = person - robot
        ts.append(step * 0.1); gaps.append(gap)
        speed = max(0.0, min(2.0, gain * (gap - 1.0)))
        robot += speed * 0.1; person += 1.0 * 0.1
    ax.plot(ts, gaps, color=colour, ls=ls, lw=2.5, label=f"gain {gain}: settles at {gaps[-1]:.2f} m")
ax.annotate("a gap stays: the robot must be\nbehind to have a reason to drive", xy=(8, 1.5), xytext=(3.6, 1.68),
            arrowprops=dict(arrowstyle="->"), fontsize=11)
ax.set_xlabel("time (seconds)"); ax.set_ylabel("distance to the person (m)")
ax.set_ylim(0.8, 1.9); ax.grid(alpha=0.3); ax.legend(loc="lower right")
save(fig, "fig06-follow-person.png")

# ---------- Figure 7: chase the ball, or aim where it will land ----------
fig, ax = plt.subplots(figsize=(10, 5.2))
ball = lambda t: min(1.2, 1.2 * t)
t, h_chase = hand_run(4, target=ball)
t2, h_aim = hand_run(4)
ax.plot(t, [ball(x) for x in t], color=GREY, lw=2, ls=":", label="ball (sideways position)")
ax.axhline(1.2, color=BLACK, ls="--", lw=2, label="landing point (setpoint when we predict)")
ax.plot(t, h_chase, color=ORANGE, lw=2.5, ls="--", label=f"hand CHASES the ball: {h_chase[-1]:.2f} m at 1 s")
ax.plot(t2, h_aim, color=BLUE, lw=2.5, label=f"hand AIMS at the landing point: {h_aim[-1]:.2f} m at 1 s")
ax.set_xlabel("time (seconds)"); ax.set_ylabel("sideways position (m)")
ax.set_ylim(0, 1.45); ax.grid(alpha=0.3); ax.legend(loc="lower right", fontsize=11)
save(fig, "fig07-chase-vs-predict.png")

print("saved 7 figures in", os.path.normpath(OUT))
