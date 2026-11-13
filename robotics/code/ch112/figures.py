# Figures for Chapter 112 - Raspberry Pi: a small computer, GPIO with Python.
# Run:  python figures.py      (saves PNG files in ../../images/ch112/; Figures 5 and 6 read the
#        jitter_gaps_*.txt files written by jitter.py)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch112")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=BLACK))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


# Figure 1: Uno and Raspberry Pi 5 side by side (log scale)
items = [("clock speed\n(MHz)", 16, 2400), ("memory (RAM)\n(KB)", 2, 4 * 1024 * 1024), ("program storage\n(KB)", 32, 32 * 1024 * 1024),
         ("power\n(mW)", 250, 5000), ("start-up time\n(ms)", 500, 20000)]
fig, ax = plt.subplots(figsize=(11, 4.6))
x = np.arange(len(items))
uno = [u for _, u, _ in items]
pi = [p for _, _, p in items]
ax.bar(x - 0.2, uno, 0.4, color=BLUE, label="Arduino Uno")
ax.bar(x + 0.2, pi, 0.4, color=RED, label="Raspberry Pi 5 (4 GB, 32 GB card)")
for k in range(len(items)):
    ax.text(k - 0.2, uno[k] * 1.3, f"{uno[k]:,}", ha="center", fontsize=9)
    ax.text(k + 0.2, pi[k] * 1.3, f"{pi[k]:,}", ha="center", fontsize=9)
ax.set_xticks(x); ax.set_xticklabels([n for n, _, _ in items], fontsize=10)
ax.set_yscale("log"); ax.set_ylim(1, 3e8); ax.set_yticks([1, 1e2, 1e4, 1e6, 1e8]); ax.set_yticklabels(["1", "100", "10,000", "1 million", "100 million"])
ax.minorticks_off(); ax.legend(fontsize=10, loc="upper left")
save(fig, "fig01-uno-vs-pi.png")

# Figure 2: the 40-pin header (the pins this course uses)
names = {1: "3V3", 2: "5V", 3: "GPIO2 SDA", 4: "5V", 5: "GPIO3 SCL", 6: "GND", 7: "GPIO4", 8: "GPIO14 TXD", 9: "GND",
         10: "GPIO15 RXD", 11: "GPIO17", 12: "GPIO18", 13: "GPIO27", 14: "GND", 15: "GPIO22", 16: "GPIO23", 17: "3V3",
         18: "GPIO24", 19: "GPIO10 MOSI", 20: "GND", 21: "GPIO9 MISO", 22: "GPIO25", 23: "GPIO11 SCLK", 24: "GPIO8 CE0",
         25: "GND", 26: "GPIO7 CE1", 27: "GPIO0", 28: "GPIO1", 29: "GPIO5", 30: "GND", 31: "GPIO6", 32: "GPIO12",
         33: "GPIO13", 34: "GND", 35: "GPIO19", 36: "GPIO16", 37: "GPIO26", 38: "GPIO20", 39: "GND", 40: "GPIO21"}
use = {11: "start button", 13: "status LED", 8: "UART to the Uno", 10: "UART to the Uno", 3: "I2C", 5: "I2C"}
fig, ax = plt.subplots(figsize=(12, 7.0))
for pin in range(1, 41):
    row = (pin - 1) // 2
    col = (pin - 1) % 2
    y = 19 - row
    xc = 5.0 + col * 0.6
    n = names[pin]
    colr = RED if n.startswith("5V") else (ORANGE if n.startswith("3V3") else (BLACK if n == "GND" else (GREEN if pin in use else L_GREY)))
    ax.add_patch(Circle((xc, y), 0.22, fc=colr, ec=BLACK))
    ax.text(xc, y, str(pin), ha="center", va="center", fontsize=6.5, color="white" if colr in (BLACK, RED, GREEN) else BLACK)
    label = n + (f"  ({use[pin]})" if pin in use else "")
    if col == 0:
        ax.text(4.65, y, label, ha="right", va="center", fontsize=8.5)
    else:
        ax.text(5.95, y, label, ha="left", va="center", fontsize=8.5)
ax.text(5.3, 20.0, "pin 1 is the square pad, near the board's corner", ha="center", fontsize=9.5)
ax.text(5.3, -1.3, "red 5 V, orange 3.3 V, black ground, green: used in this course.  Every GPIO pin works at 3.3 V only.",
        ha="center", fontsize=10)
ax.set_xlim(0.5, 10); ax.set_ylim(-1.8, 20.5); ax.axis("off")
save(fig, "fig02-header.png")

# Figure 6: why Rover has both
fig, ax = plt.subplots(figsize=(12, 4.4))
box(ax, 0.0, 0.5, 4.6, 3.2, "", L_RED)
ax.text(2.3, 3.35, "Raspberry Pi: thinking", ha="center", fontsize=12)
ax.text(0.25, 1.95, "camera and vision\nmaps and planning\nPython, ROS 2, Wi-Fi\nlogs and files\n\nfast, but timing wobbles",
        va="center", fontsize=10.5)
box(ax, 7.4, 0.5, 4.6, 3.2, "", L_BLUE)
ax.text(9.7, 3.35, "Arduino Uno: real time", ha="center", fontsize=12)
ax.text(7.65, 1.95, "encoders (interrupts)\nmotor PWM, 100 Hz control\nbumpers, battery\nfailsafe stop\n\nslow, but exactly on time",
        va="center", fontsize=10.5)
ax.add_patch(FancyArrowPatch((4.7, 2.4), (7.3, 2.4), arrowstyle="-|>", mutation_scale=14, lw=2, color=BLACK))
ax.add_patch(FancyArrowPatch((7.3, 1.7), (4.7, 1.7), arrowstyle="-|>", mutation_scale=14, lw=2, color=BLACK))
ax.text(6.0, 2.6, "M packets: wheel speeds", ha="center", fontsize=9.5)
ax.text(6.0, 1.35, "S packets: status", ha="center", fontsize=9.5)
ax.text(6.0, 0.6, "UART or USB\n(Chapters 107, 111)", ha="center", fontsize=9.5)
ax.set_xlim(-0.2, 12.2); ax.set_ylim(0.3, 3.9); ax.axis("off")
save(fig, "fig06-rover-split.png")

# Figure 4: the start-button program on the mock (from its printed output)
fig, ax = plt.subplots(figsize=(11, 3.6))
led = [(0, 1), (0.2, 0), (1.0, 1), (1.2, 0), (1.5, 1), (4.2, 0), (5.0, 1), (5.2, 0), (5.5, 0)]
xs, ys = zip(*led)
ax.step(xs, np.array(ys) + 1.5, where="post", color=ORANGE, lw=2)
btn = [(0, 0), (1.5, 1), (1.8, 0), (4.0, 1), (4.1, 0), (5.5, 0)]
xs, ys = zip(*btn)
ax.step(xs, ys, where="post", color=BLUE, lw=2)
ax.text(-0.1, 2.0, "status LED\n(GPIO 27)", ha="right", va="center", fontsize=10)
ax.text(-0.1, 0.5, "button\n(GPIO 17)", ha="right", va="center", fontsize=10)
ax.text(1.55, 3.0, "start: steady", fontsize=10, color=GREEN); ax.text(4.05, 3.0, "stop: blinking again", fontsize=10, color=RED)
ax.set_xlim(-1.1, 5.6); ax.set_ylim(-0.3, 3.3); ax.set_yticks([]); ax.set_xlabel("time (s)")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig04-start-button.png")


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return np.array([float(v) for v in f.read().split()])


# Figure 3: the 10 ms loop on a PC with an operating system, against the Uno's timer (Chapter 106)
g10 = load("jitter_gaps_10ms.txt") / 1000
fig, ax = plt.subplots(figsize=(11, 4.4))
ax.plot(np.arange(1, len(g10) + 1), g10, color=RED, lw=1, label="Python loop on a PC with an operating system (measured)")
ax.plot([1, len(g10)], [10, 10], color=GREEN, lw=2.5, label="Uno, Timer1 interrupt (Chapter 106): 10.000 ms every time")
ax.set_xlabel("step number"); ax.set_ylabel("gap since the previous step (ms)"); ax.legend(fontsize=10, loc="upper right")
ax.set_ylim(0, max(g10) * 1.15); ax.grid(alpha=0.3)
save(fig, "fig03-jitter-10ms.png")

# Figure 5: how the gaps of the 1 ms loop are spread
g1 = load("jitter_gaps_1ms.txt")
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.hist(g1, bins=60, color=BLUE)
ax.axvline(1000, color=GREEN, lw=2); ax.text(1010, ax.get_ylim()[1] * 0.9, "target 1,000 us", color=GREEN, fontsize=10)
ax.axvline(1100, color=RED, ls="--", lw=1.5); ax.text(1110, ax.get_ylim()[1] * 0.75, "10 % late", color=RED, fontsize=10)
ax.set_xlabel("gap between steps (us)"); ax.set_ylabel("how many steps")
save(fig, "fig05-jitter-1ms.png")
print("figures saved in", os.path.abspath(OUT))
