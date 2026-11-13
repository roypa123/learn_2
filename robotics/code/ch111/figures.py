# Figures for Chapter 111 - Arduino talking to Python (pyserial).
# Run:  python figures.py      (saves PNG files in ../../images/ch111/; Figure 4 reads joint_log.csv,
#        made by stream_logger.py)
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch111")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=11, family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=BLACK))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, family=family)


def arrow(ax, a, b, col=BLACK, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=13, lw=1.6, color=col))


# Figure 1: opening the port resets the Uno
fig, ax = plt.subplots(figsize=(12, 3.6))
ax.add_patch(Rectangle((0, 1.0), 0.5, 0.8, fc=L_RED, ec=RED)); ax.text(0.25, 1.4, "boot-\nloader\n0.5 s", ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((0.5, 1.0), 3.5, 0.8, fc=L_GREEN, ec=GREEN)); ax.text(3.0, 1.4, "your sketch: setup(), loop() ...", ha="center", va="center", fontsize=10.5)
ax.plot([0, 0], [0.6, 2.3], color=BLACK, lw=2); ax.text(0.02, 2.4, "Python opens the port: DTR pulse -> the Uno resets", fontsize=10.5)
ax.plot([2.0, 2.0], [0.6, 2.0], color=BLUE, lw=2, ls="--"); ax.text(2.03, 2.05, "time.sleep(2) ends: safe to talk (a margin for slower boards)", fontsize=10.5, color=BLUE)
ax.text(0.25, 0.7, "bytes sent now\nare lost", ha="center", fontsize=9.5, color=RED)
ax.set_xlim(-0.1, 4.1); ax.set_ylim(0.4, 2.7); ax.set_yticks([]); ax.set_xlabel("seconds after opening the port")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig01-reset.png")

# Figure 2: from bytes to numbers
fig, ax = plt.subplots(figsize=(12, 3.4))
steps = [("b'1400,162.8\\r\\n'", "ser.readline()\nbytes", L_GREY), ("'1400,162.8'", ".decode() .strip()\ntext", L_BLUE),
         ("['1400', '162.8']", ".split(',')\na list of text", L_ORANGE), ("1400   162.8", "int()  float()\nnumbers", L_GREEN)]
for k, (val, how, col) in enumerate(steps):
    x = k * 3.1
    box(ax, x, 1.0, 2.6, 0.8, val, col, 11, "monospace")
    ax.text(x + 1.3, 0.5, how, ha="center", va="center", fontsize=10)
    if k:
        arrow(ax, (x - 0.45, 1.4), (x - 0.05, 1.4))
ax.set_xlim(-0.2, 12.3); ax.set_ylim(0.0, 2.0); ax.axis("off")
save(fig, "fig02-parse.png")

# Figure 3: how this chapter's outputs were made
fig, ax = plt.subplots(figsize=(12, 4.4))
box(ax, 0.0, 2.6, 3.0, 1.0, "your Python program\n(stream_logger.py)", L_BLUE, 10.5)
box(ax, 4.2, 2.6, 3.2, 1.0, "pyserial\n(import serial)", L_GREY, 10.5)
box(ax, 8.6, 2.6, 3.0, 1.0, "USB cable ->\na real Uno", L_GREEN, 10.5)
arrow(ax, (3.05, 3.1), (4.15, 3.1)); arrow(ax, (7.45, 3.1), (8.55, 3.1))
ax.text(5.8, 3.85, "with hardware", ha="center", fontsize=11, color=GREEN)
box(ax, 0.0, 0.3, 3.0, 1.0, "the same program,\nunchanged", L_BLUE, 10.5)
box(ax, 4.2, 0.3, 3.2, 1.0, "bench_serial.py\n(pyserial's stand-in)", L_ORANGE, 10.5)
box(ax, 8.6, 0.3, 3.0, 1.0, "the real sketch on\nthe PC test bench", L_ORANGE, 10.5)
arrow(ax, (3.05, 0.8), (4.15, 0.8)); arrow(ax, (7.45, 0.8), (8.55, 0.8), style="<|-|>")
ax.text(8.0, 1.05, "pipe", ha="center", fontsize=9.5)
ax.text(5.8, 1.55, "without hardware (this chapter's outputs): one shared simulated clock", ha="center", fontsize=11, color=ORANGE)
ax.set_xlim(-0.2, 11.8); ax.set_ylim(0.1, 4.2); ax.axis("off")
save(fig, "fig03-bench-link.png")

# Figure 4: the logged joint angle
ts, angles = [], []
with open(os.path.join(HERE, "joint_log.csv")) as f:
    for row in csv.DictReader(f):
        ts.append(int(row["time_ms"]) / 1000)
        angles.append(float(row["angle_deg"]))
fig, ax = plt.subplots(figsize=(10, 4.2))
x = np.linspace(min(ts), max(ts), 400)
ax.plot(x, 135 + 90 * np.sin(2 * np.pi * 0.5 * x), color=GREY, ls="--", lw=1.5, label="the joint's real angle")
ax.plot(ts, angles, "o", color=BLUE, ms=5, label="logged by stream_logger.py")
ax.set_xlabel("sketch time (s)"); ax.set_ylabel("angle (degrees)"); ax.grid(alpha=0.3)
ax.legend(fontsize=10, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.0))
save(fig, "fig04-joint-log.png")

# Figure 5: commands and replies (rover_driver.py on the bench)
fig, ax = plt.subplots(figsize=(12, 4.0))
sent = [0, 100.1, 200.2, 300.3, 400.4, 500.5, 600.6, 700.7]
cmds = [(0, 0), (60, 60), (120, 120), (180, 180), (200, 200), (200, 120), (200, 60), (150, 150)]
for t, (l, r) in zip(sent, cmds):
    arrow(ax, (t, 2.0), (t + 0.75, 1.0), BLUE)
    ax.text(t, 2.12, f"M {l},{r}", fontsize=8.5, ha="center", color=BLUE, rotation=35)
    arrow(ax, (t + 0.8, 1.0), (t + 30, 2.0), GREEN)
ax.text(1201.2, 2.12, "S 0,0\n(failsafe)", fontsize=9, ha="center", color=RED)
arrow(ax, (1200.5, 1.0), (1225, 2.0), RED)
ax.plot([700.7, 1200.5], [0.85, 0.85], color=RED, lw=1.5); ax.text(950, 0.65, "500 ms without a command", ha="center", fontsize=9.5, color=RED)
ax.axhline(2.0, color=GREY, lw=1); ax.axhline(1.0, color=GREY, lw=1)
ax.text(-120, 2.0, "Pi", va="center", fontsize=11); ax.text(-150, 1.0, "Uno", va="center", fontsize=11)
ax.set_xlim(-170, 1320); ax.set_ylim(0.4, 2.8); ax.set_yticks([]); ax.set_xlabel("time (ms) after the 2 s wait")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig05-driver.png")

# Figure 6: without the wait, every command falls inside the bootloader
fig, ax = plt.subplots(figsize=(12, 3.0))
ax.add_patch(Rectangle((0, 1.0), 500, 0.6, fc=L_RED, ec=RED)); ax.text(250, 1.3, "bootloader", ha="center", va="center", fontsize=10.5)
ax.add_patch(Rectangle((500, 1.0), 800, 0.6, fc=L_GREEN, ec=GREEN)); ax.text(900, 1.3, "rover_link runs", ha="center", va="center", fontsize=10)
for t in sent:
    ax.plot([t, t], [1.7, 2.1], color=RED if t < 500 else GREEN, lw=2.5)
ax.text(0, 2.25, "rover_driver.py --no-wait: the first 5 commands are lost (red); the last 3 arrive and are answered (green)", fontsize=10.5)
ax.set_xlim(-50, 1350); ax.set_ylim(0.8, 2.6); ax.set_yticks([]); ax.set_xlabel("ms after opening the port")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig06-no-wait.png")
print("figures saved in", os.path.abspath(OUT))
