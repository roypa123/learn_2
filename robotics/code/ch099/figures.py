# Figures for Chapter 99 - Reading buttons: digital input and debouncing.
# Run:  python figures.py      (saves PNG files in ../../images/ch099/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch, Polygon, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch099")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"
EDGES = [0.0, 0.08, 0.15, 0.35, 0.45, 0.70, 0.85]     # the same bounce as sim_inputs.h


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def wire(ax, pts, color=BLACK, lw=2):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, solid_capstyle="round")


def resistor_v(ax, x, y0, y1, label):
    ys = np.linspace(y0 - 0.12, y1 + 0.12, 13)
    xs = [x] + [x + (0.12 if k % 2 else -0.12) for k in range(1, 12)] + [x]
    wire(ax, [(x, y0), (x, y0 - 0.12)]); wire(ax, list(zip(xs, ys))); wire(ax, [(x, y1 + 0.12), (x, y1)])
    ax.text(x + 0.22, (y0 + y1) / 2, label, va="center", fontsize=10)


def button_v(ax, x, y0, y1):
    wire(ax, [(x, y0), (x, y0 - 0.25)]); wire(ax, [(x, y1), (x, y1 + 0.25)])
    wire(ax, [(x - 0.25, y0 - 0.25), (x + 0.05, y1 + 0.32)], lw=2.2)
    ax.text(x - 0.35, (y0 + y1) / 2, "button", ha="right", va="center", fontsize=10)


def ground(ax, x, y):
    for k, w in enumerate([0.25, 0.16, 0.08]):
        wire(ax, [(x - w, y - k * 0.09), (x + w, y - k * 0.09)], lw=1.8)


def pin(ax, x, y, label="pin 2"):
    ax.add_patch(Rectangle((x - 0.45, y - 0.22), 0.9, 0.44, fc=GREY, ec=BLACK)); ax.text(x, y, label, ha="center", va="center", fontsize=9.5)


def bounce_level(ms, down, up, b=3.0):
    """Python copy of sim::bouncy_button for one press: 1 = HIGH (free), 0 = LOW (pressed)."""
    if down <= ms < up:
        x = (ms - down) / b
        if x >= 1:
            return 0
        k = sum(1 for e in EDGES if e <= x)
        return 0 if k % 2 == 1 else 1
    if up <= ms < up + b:
        x = (ms - up) / b
        k = sum(1 for e in EDGES if e <= x)
        return 1 if k % 2 == 1 else 0
    return 1


# Figure 1: three ways to connect a button
fig, axes = plt.subplots(1, 3, figsize=(13, 5.4))
ax = axes[0]
pin(ax, 1.0, 3.5); wire(ax, [(1.45, 3.5), (2.5, 3.5), (2.5, 3.2)]); button_v(ax, 2.5, 3.2, 1.6)
wire(ax, [(2.5, 1.6), (2.5, 1.2)]); ax.text(2.5, 1.0, "5 V", ha="center", fontsize=11)
ax.text(1.8, 0.2, "free: pin connected to NOTHING\n-> floating, reads anything", ha="center", fontsize=10.5, color=RED)
ax.set_title("no resistor: WRONG", fontsize=12, color=RED)
ax = axes[1]
wire(ax, [(2.5, 4.6), (2.5, 4.3)]); ax.text(2.5, 4.75, "5 V", ha="center", fontsize=11)
button_v(ax, 2.5, 4.3, 2.9); wire(ax, [(2.5, 2.9), (2.5, 2.6)]); wire(ax, [(2.5, 2.75), (1.45, 2.75)]); pin(ax, 1.0, 2.75)
resistor_v(ax, 2.5, 2.6, 1.4, "10 k\npull-down"); ground(ax, 2.5, 1.4)
ax.text(1.8, 0.2, "free: LOW    pressed: HIGH\n(active-high, Chapter 83)", ha="center", fontsize=10.5)
ax.set_title("external pull-down", fontsize=12)
ax = axes[2]
ax.add_patch(FancyBboxPatch((0.1, 2.0), 1.6, 2.6, boxstyle="round,pad=0.02", fc=L_BLUE, ec=BLUE, ls="--"))
ax.text(0.9, 4.4, "inside the chip", ha="center", fontsize=9.5, color=BLUE)
wire(ax, [(1.2, 4.2), (1.2, 3.9)]); ax.text(1.55, 4.2, "5 V", fontsize=10)
resistor_v(ax, 1.2, 3.9, 2.9, "20-50 k")
wire(ax, [(1.2, 2.9), (1.2, 2.6), (2.5, 2.6), (2.5, 2.4)]); pin(ax, 0.75, 2.4)
button_v(ax, 2.5, 2.4, 1.2); ground(ax, 2.5, 1.2)
ax.text(1.8, 0.2, "free: HIGH    pressed: LOW\npinMode(2, INPUT_PULLUP)", ha="center", fontsize=10.5, color=GREEN)
ax.set_title("INPUT_PULLUP: no extra parts", fontsize=12, color=GREEN)
for ax in axes:
    ax.set_xlim(-0.2, 3.8); ax.set_ylim(-0.3, 5.0); ax.axis("off")
save(fig, "fig01-three-wirings.png")

# Figure 2: one press, zoomed in: the contacts bounce
t = np.linspace(-1, 9, 4000)
raw = np.array([bounce_level(x, 0.0, 1000.0) for x in t])
fig, axes = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True)
axes[0].plot(t, raw * 5, color=BLUE, lw=2, drawstyle="steps-post")
falls = [t[k] for k in range(1, len(t)) if raw[k - 1] == 1 and raw[k] == 0]
for f in falls:
    axes[0].annotate("", xy=(f, 0.2), xytext=(f, -1.3), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.5))
axes[0].text(4.2, -1.1, f"a raw edge detector counts {len(falls)} presses here", color=RED, fontsize=11)
axes[0].set_ylabel("pin 2 (V)"); axes[0].set_ylim(-1.6, 6.0); axes[0].grid(alpha=0.3)
axes[0].set_title("one press of the button, zoomed in to 10 ms (the bounce model of the PC test bench)", fontsize=11)
deb = np.ones_like(t)
last_change, last, stable = -10.0, 1, 1
for k, x in enumerate(t):
    if raw[k] != last:
        last, last_change = raw[k], x
    if x - last_change >= 5.0 and raw[k] != stable:
        stable = raw[k]
    deb[k] = stable
axes[1].plot(t, deb * 5, color=GREEN, lw=2.5, drawstyle="steps-post")
axes[1].axvspan(2.55, 7.55, color=L_GREEN)
axes[1].text(5.05, 2.5, "steady for 5 ms", ha="center", fontsize=11)
axes[1].set_ylabel("debounced"); axes[1].set_ylim(-0.5, 6.0); axes[1].grid(alpha=0.3); axes[1].set_xlabel("time after the press (ms)")
save(fig, "fig03-bounce.png")

# Figure 3: edge detection: compare this level with the last one
fig, ax = plt.subplots(figsize=(11, 4.0))
ts = [0, 1, 1, 3, 3, 5]
lv = [1, 1, 0, 0, 1, 1]
ax.plot(ts, lv, color=BLUE, lw=3)
ax.annotate("last = HIGH, now = LOW\n-> the press EDGE (count it once)", xy=(1, 0.5), xytext=(1.3, 0.75), fontsize=11, color=RED,
            arrowprops=dict(arrowstyle="-|>", color=RED))
ax.annotate("last = LOW, now = HIGH\n-> the release edge", xy=(3, 0.5), xytext=(3.3, 0.25), fontsize=11, color=ORANGE,
            arrowprops=dict(arrowstyle="-|>", color=ORANGE))
ax.text(2.0, 0.1, "pressed: LOW on every pass,\nbut only ONE edge", ha="center", fontsize=10.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(["LOW\n(pressed)", "HIGH\n(free)"]); ax.set_ylim(-0.2, 1.3)
ax.set_xticks([]); ax.set_xlabel("time")
save(fig, "fig02-edges.png")

# Figure 4: counts with and without debouncing (numbers from the PC test bench)
fig, ax = plt.subplots(figsize=(11, 4.6))
names = ["5 real presses\n(3 ms bounce)\nno debounce", "5 real presses\n(3 ms bounce)\n5 ms debounce",
         "worn switch\n(50 ms bounce)\n5 ms debounce", "worn switch\n(50 ms bounce)\n10 ms debounce"]
vals = [35, 5, 25, 5]
cols = [RED, GREEN, RED, GREEN]
bars = ax.bar(range(4), vals, color=cols)
for k, v in enumerate(vals):
    ax.text(k, v + 0.8, str(v), ha="center", fontsize=13, weight="bold")
ax.axhline(5, color=BLACK, ls="--", lw=1.3); ax.text(3.45, 6.0, "true: 5", fontsize=11, ha="right")
ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=10); ax.set_ylabel("presses counted"); ax.set_ylim(0, 40)
ax.grid(axis="y", alpha=0.3)
save(fig, "fig04-counts.png")

# Figure 5: polling slowly misses short presses (slow_poll.ino, WORK_MS = 200)
downs = [250, 830, 1410, 2120, 2700, 3390, 4050, 4610]
fig, ax = plt.subplots(figsize=(12, 3.8))
for d in downs:
    ax.add_patch(Rectangle((d, 0.6), 60, 0.8, fc=L_ORANGE, ec=ORANGE))
polls = []
tt = 0.0
while tt < 5000:
    polls.append(tt)
    tt += 200.03
for p in polls:
    hit = any(d <= p < d + 60 for d in downs)
    ax.plot([p, p], [0.3, 1.7], color=GREEN if hit else GREY, lw=2.5 if hit else 1)
ax.text(3400, 1.85, "the only press seen", color=GREEN, ha="center", fontsize=11)
ax.text(0, 2.25, "orange: the 8 presses (60 ms each)     grey lines: the moments loop() reads the button (every 200 ms)", fontsize=10.5)
ax.set_xlim(0, 5000); ax.set_ylim(0, 2.5); ax.set_yticks([]); ax.set_xlabel("time (ms)")
save(fig, "fig05-polling.png")

# Figure 6: Rover's bumpers from above
fig, ax = plt.subplots(figsize=(10, 6))
ax.add_patch(FancyBboxPatch((3, 1), 4, 3, boxstyle="round,pad=0.05,rounding_size=0.4", fc=L_ORANGE, ec=BLACK, lw=2))
ax.text(5, 2.3, "Rover\n(seen from above)", ha="center", va="center", fontsize=12)
for x in (2.7, 7.0):
    ax.add_patch(Rectangle((x, 1.4), 0.3, 1.2, fc="#444444", ec=BLACK))
ax.plot([3.1, 4.9], [4.35, 4.35], color=BLUE, lw=6); ax.plot([5.1, 6.9], [4.35, 4.35], color=RED, lw=6)
ax.text(4.0, 4.65, "left bumper\n(pin 4)", ha="center", fontsize=11, color=BLUE)
ax.text(6.0, 4.65, "right bumper\n(pin 7)", ha="center", fontsize=11, color=RED)
ax.annotate("", xy=(5, 5.9), xytext=(5, 4.9), arrowprops=dict(arrowstyle="-|>", lw=2))
ax.text(5.15, 5.6, "forward", fontsize=10.5)
ax.text(0.2, 3.2, "left bump:\nback up,\nthen turn\nRIGHT", fontsize=10.5, color=BLUE)
ax.text(8.4, 3.2, "right bump:\nback up,\nthen turn\nLEFT", fontsize=10.5, color=RED)
ax.set_xlim(0, 10.5); ax.set_ylim(0.5, 6.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-bumpers.png")

# Figure 7: the bumper test timeline (pc_tests/test_bumpers.cpp)
fig, ax = plt.subplots(figsize=(11, 3.6))
for row, (name, spans, col) in enumerate([("left (pin 4)", [(1000, 1300), (3000, 3400)], BLUE),
                                           ("right (pin 7)", [(2000, 2200), (3010, 3400)], RED)]):
    for a, b in spans:
        ax.add_patch(Rectangle((a, 1 - row), b - a, 0.6, fc=col, ec=BLACK))
    ax.text(950, 1 - row + 0.3, name, ha="right", va="center", fontsize=11)
for t_ms, msg in [(1007, "left: turn right"), (2007, "right: turn left"), (3007, "left: turn right"), (3017, "both: turn around")]:
    ax.axvline(t_ms, color=GREEN, ls=":", lw=1.5)
for t_ms, msg, y in [(1007, "1007 ms: left, turn right", 1.9), (2007, "2007 ms: right, turn left", 1.9), (3007, "3007 ms: left", 1.9),
                     (3017, "3017 ms: both, turn around", 2.25)]:
    ax.text(t_ms + 15, y, msg, fontsize=10, color=GREEN)
ax.set_xlim(600, 3900); ax.set_ylim(-0.2, 2.6); ax.set_yticks([]); ax.set_xlabel("time (ms)")
save(fig, "fig07-bumper-timeline.png")
print("figures saved in", os.path.abspath(OUT))
