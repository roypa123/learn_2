# Figures for Chapter 100 - The serial monitor: talking to the computer.
# Run:  python figures.py      (saves PNG files in ../../images/ch100/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch100")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(ax, x1, y1, x2, y2, color=BLACK):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=15, color=color, lw=1.8))


# Figure 1: the path of a character from the sketch to the Serial Monitor and back
fig, ax = plt.subplots(figsize=(13, 4.4))
steps = [("Serial.print(\"Hi\")\nin your sketch", L_ORANGE), ("transmit buffer\n64 bytes", L_GREEN), ("UART hardware\n(Chapter 107)\npins 0 and 1", L_GREY),
         ("USB chip\n(16U2 or CH340)", L_GREY), ("USB cable", L_GREY), ("Serial Monitor\non the computer", L_BLUE)]
for k, (t, c) in enumerate(steps):
    box(ax, k * 2.2, 2.0, 1.9, 1.3, t, c)
    if k:
        arrow(ax, k * 2.2 - 0.28, 2.85, k * 2.2 - 0.02, 2.85, color=BLUE)
for k in range(1, 6):
    arrow(ax, k * 2.2 - 0.02, 2.4, k * 2.2 - 0.28, 2.4, color=RED)
ax.text(5.6, 3.65, "out: what the sketch prints (the TX LED flashes)", ha="center", fontsize=11, color=BLUE)
ax.text(5.6, 1.55, "in: what you type (the RX LED flashes) -> receive buffer, 64 bytes -> Serial.read()", ha="center", fontsize=11, color=RED)
ax.set_xlim(-0.2, 13.2); ax.set_ylim(1.2, 4.0); ax.axis("off")
save(fig, "fig01-serial-path.png")

# Figure 2: the letter R on the wire at 9600 baud
bits = [0] + [int(b) for b in format(ord("R"), "08b")[::-1]] + [1]          # start, 8 data bits (lowest first), stop
names = ["start"] + [f"bit {k}" for k in range(8)] + ["stop"]
fig, ax = plt.subplots(figsize=(13, 4.0))
ts, vs = [-1.0, 0.0], [1, 1]
for k, b in enumerate(bits):
    ts += [k, k + 1]; vs += [b, b]
ts += [10, 11]; vs += [1, 1]
ax.plot(ts, [5 * v for v in vs], color=BLUE, lw=2.5, drawstyle="steps-pre")
for k, (b, n) in enumerate(zip(bits, names)):
    ax.text(k + 0.5, 5.6, n, ha="center", fontsize=9.5)
    ax.text(k + 0.5, -0.9, str(b), ha="center", fontsize=12, weight="bold", color=GREEN if 0 < k < 9 else GREY)
    ax.axvline(k, color=GREY, lw=0.6, ls=":")
ax.annotate("", xy=(1, 6.5), xytext=(0, 6.5), arrowprops=dict(arrowstyle="<->"))
ax.text(0.5, 6.7, "104 us", ha="center", fontsize=10)
ax.text(5, -1.9, "'R' = 82 = 0101 0010 in binary; the lowest bit is sent first. 10 bits = 1.04 ms at 9600 baud.", ha="center", fontsize=11)
ax.set_xlim(-1, 11); ax.set_ylim(-2.4, 7.4); ax.set_yticks([0, 5]); ax.set_yticklabels(["0 V", "5 V"])
ax.set_xticks([])
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
save(fig, "fig02-letter-on-wire.png")

# Figure 3: how long print takes (print_cost.ino on the PC test bench)
chars = [10, 60, 100, 200]
t9600 = [53, 303, 36701, 140847]
t115 = [53, 303, 3064, 11746]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(chars, [t / 1000 for t in t9600], "o-", color=RED, lw=2.5, label="9600 baud")
ax.plot(chars, [t / 1000 for t in t115], "s--", color=BLUE, lw=2.5, label="115200 baud")
ax.axvline(64, color=BLACK, ls=":", lw=1.5); ax.text(66, 120, "64: the transmit\nbuffer is full", fontsize=11)
ax.set_xlabel("characters printed in one go"); ax.set_ylabel("time inside Serial.print (ms)")
ax.legend(loc="upper left", fontsize=11); ax.grid(alpha=0.3)
save(fig, "fig03-print-cost.png")

# Figure 4: what the Serial Plotter draws for plotter.ino
rows = []
for line in open(os.path.join(HERE, "pc_tests", "plotter_output.txt")):
    parts = dict(p.split(":") for p in line.strip().split(","))
    rows.append((float(parts["wave"]), float(parts["noisy"])))
fig, ax = plt.subplots(figsize=(11, 4.6))
ax.set_facecolor("#FCFCFC")
ax.plot([r[1] for r in rows], color=ORANGE, lw=1.5, label="noisy")
ax.plot([r[0] for r in rows], color=BLUE, lw=2.5, label="wave")
ax.set_xlabel("sample number (one per println)"); ax.set_ylabel("value")
ax.legend(loc="upper right", fontsize=11); ax.grid(alpha=0.3)
ax.set_title("Serial Plotter view of plotter.ino: one line per name, a new point per println", fontsize=11)
save(fig, "fig04-plotter.png")

# Figure 5: the command parser, character by character, for "F 120"
chars_in = ["F", " ", "1", "2", "0", "\\n"]
cmd = ["F", "F", "F", "F", "F", "F: run it!"]
num = ["0", "0", "1", "12", "120", "120, then 0"]
fig, ax = plt.subplots(figsize=(12, 3.6))
for k, (c, a, n) in enumerate(zip(chars_in, cmd, num)):
    x = k * 1.9
    ax.add_patch(Rectangle((x, 2.0), 1.6, 0.8, fc=L_BLUE, ec=BLACK)); ax.text(x + 0.8, 2.4, f"'{c}'", ha="center", va="center", fontsize=13, family="monospace")
    ax.text(x + 0.8, 1.55, f"command = {a}", ha="center", fontsize=10)
    ax.text(x + 0.8, 1.1, f"number = {n}", ha="center", fontsize=10)
    if k:
        arrow(ax, x - 0.28, 2.4, x - 0.02, 2.4)
ax.text(-0.1, 3.1, "characters arrive one by one; each pass of loop() handles the ones that are already there", fontsize=11)
ax.text(5.6, 0.45, "number = number x 10 + digit:   0 -> 1 -> 12 -> 120", ha="center", fontsize=11, color=GREEN)
ax.set_xlim(-0.2, 11.4); ax.set_ylim(0.2, 3.4); ax.axis("off")
save(fig, "fig05-parser.png")

# Figure 6: the logger falls behind at 9600 baud (log_csv.ino on the PC test bench)
fig, ax = plt.subplots(figsize=(10, 4.8))
for fname, col, ls, label in [("log_9600_output.txt", RED, "-", "9600 baud"), ("log_115200_output.txt", BLUE, "--", "115200 baud")]:
    lines = open(os.path.join(HERE, "pc_tests", fname)).read().split("\n")[1:]
    t = [int(l.split(",")[0]) for l in lines if l.strip()]
    ax.plot(range(len(t)), [ti - 20 * k for k, ti in enumerate(t)], color=col, ls=ls, lw=2.5, label=label)
ax.set_xlabel("line number"); ax.set_ylabel("how late the line is (ms)")
ax.legend(loc="upper left", fontsize=11); ax.grid(alpha=0.3)
save(fig, "fig06-logger-lag.png")

# Figure 7: how busy the link is at each baud rate (serial_budget.py)
bauds = ["9600", "19200", "57600", "115200"]
busy = [120, 60, 20, 10]
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.bar(bauds, busy, color=[RED, GREEN, GREEN, GREEN])
for k, b in enumerate(busy):
    ax.text(k, b + 3, f"{b}%", ha="center", fontsize=12)
ax.axhline(100, color=BLACK, ls="--"); ax.text(3.4, 103, "100%: full", ha="right", fontsize=11)
ax.set_xlabel("baud rate"); ax.set_ylabel("link busy (%)"); ax.set_ylim(0, 135)
ax.set_title("50 lines of 23 characters per second", fontsize=12)
save(fig, "fig07-link-busy.png")
print("figures saved in", os.path.abspath(OUT))
