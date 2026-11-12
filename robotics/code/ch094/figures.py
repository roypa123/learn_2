# Figures for Chapter 94 - What is a microcontroller?
# Run:  python figures.py      (saves PNG files in ../../images/ch094/)
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle
from matplotlib.ticker import NullFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch094")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, ec=BLACK, fs=12, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight)


def arrow(ax, x1, y1, x2, y2, color=BLACK, lw=1.8, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16,
                                 color=color, lw=lw))


def chip(ax, x, y, s=0.32):
    ax.add_patch(Rectangle((x, y), s, s, fc="#333333", ec=BLACK))
    for k in range(3):
        for side in (-1, 1):
            yy = y + s * (0.2 + 0.3 * k)
            xx = x - 0.07 if side < 0 else x + s
            ax.add_patch(Rectangle((xx, yy - 0.015), 0.07, 0.03, fc=GREY, ec=GREY))


# Figure 1: microcontrollers hide everywhere
fig, ax = plt.subplots(figsize=(11, 5.6))
things = [("TV remote", "1", L_GREY), ("microwave oven", "1", L_GREY), ("washing machine", "2-3", L_GREY),
          ("robot vacuum", "3-6", L_ORANGE), ("drone", "5 or more", L_ORANGE), ("modern car", "70 or more", L_GREY),
          ("Moth (Ch 93)", "0", L_RED), ("Rover", "1 + a Raspberry Pi", L_ORANGE)]
for k, (name, n, col) in enumerate(things):
    x, y = (k % 4) * 2.75, 2.6 - (k // 4) * 2.5
    box(ax, x, y, 2.45, 2.0, "", col)
    ax.text(x + 1.225, y + 1.62, name, ha="center", fontsize=13, weight="bold")
    if n != "0":
        chip(ax, x + 1.06, y + 0.82)
    else:
        ax.text(x + 1.225, y + 0.98, "only wires and\ntransistors", ha="center", va="center", fontsize=11)
    ax.text(x + 1.225, y + 0.38, "microcontrollers:\n" + n, ha="center", va="center", fontsize=11)
ax.set_xlim(-0.2, 11); ax.set_ylim(-0.1, 4.8); ax.axis("off")
ax.set_title("Small computers on one chip are inside almost every machine that has buttons or moves", fontsize=13)
save(fig, "fig01-mcus-everywhere.png")

# Figure 2: inside a microcontroller
fig, ax = plt.subplots(figsize=(11, 6.6))
ax.add_patch(Rectangle((0.6, 0.6), 9.8, 5.6, fc="#F4F4F4", ec=BLACK, lw=2.5))
ax.text(5.5, 5.85, "ATmega328P - the chip on the Arduino Uno (one piece of silicon)", ha="center", fontsize=13, weight="bold")
for k in range(14):                       # pins on the edges
    xx = 1.0 + k * 0.67
    ax.add_patch(Rectangle((xx, 6.2), 0.18, 0.35, fc=GREY, ec=BLACK))
    ax.add_patch(Rectangle((xx, 0.25), 0.18, 0.35, fc=GREY, ec=BLACK))
ax.text(5.5, 6.85, "pins: the chip's legs to the outside world", ha="center", fontsize=11)
box(ax, 4.1, 3.2, 2.8, 1.6, "CPU\nfollows the program\none step at a time", L_ORANGE, fs=12, weight="bold")
box(ax, 0.9, 4.0, 2.6, 1.2, "FLASH 32 KB\nthe program\n(kept without power)", L_BLUE, fs=11)
box(ax, 0.9, 2.5, 2.6, 1.2, "SRAM 2 KB\nvariables\n(lost without power)", L_GREEN, fs=11)
box(ax, 0.9, 1.0, 2.6, 1.2, "EEPROM 1 KB\nsaved settings\n(kept without power)", L_GREY, fs=11)
box(ax, 7.6, 4.3, 2.5, 0.9, "clock 16 MHz\n(the heartbeat)", L_RED, fs=11)
periph = ["digital in/out", "ADC (analog in)", "timers + PWM", "UART  I2C  SPI"]
for k, p in enumerate(periph):
    box(ax, 7.6, 3.2 - k * 0.72, 2.5, 0.58, p, L_GREEN if k < 2 else L_BLUE, fs=11)
ax.plot([3.8, 3.8], [1.6, 4.6], color=BLACK, lw=4)          # the bus
ax.plot([7.2, 7.2], [0.98, 4.75], color=BLACK, lw=4)
for yy in (4.6, 3.1, 1.6):
    arrow(ax, 3.5, yy, 3.8, yy, style="<|-|>")
arrow(ax, 6.9, 4.0, 7.2, 4.0, style="<|-|>"); arrow(ax, 3.8, 4.0, 4.1, 4.0, style="<|-|>")
for k in range(4):
    arrow(ax, 7.2, 3.49 - k * 0.72, 7.6, 3.49 - k * 0.72, style="<|-|>")
arrow(ax, 7.2, 4.75, 7.6, 4.75, style="<|-|>")
ax.text(3.8, 1.25, "bus", ha="center", fontsize=11); ax.text(7.2, 0.75, "bus", ha="center", fontsize=11)
ax.set_xlim(0.3, 10.7); ax.set_ylim(0, 7.1); ax.axis("off")
save(fig, "fig02-inside-mcu.png")

# Figure 3: fetch, decode, execute with the toy program
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw={"width_ratios": [1, 1.35]})
for (x, y, t, c) in [(0, 1.2, "1. FETCH\nread the next\ninstruction", L_BLUE), (1.2, -0.8, "2. DECODE\nwhat does it\nmean?", L_ORANGE),
                     (-1.2, -0.8, "3. EXECUTE\ndo it, then\ngo to the next", L_GREEN)]:
    a1.add_patch(Circle((x, y), 0.82, fc=c, ec=BLACK, lw=1.5))
    a1.text(x, y, t, ha="center", va="center", fontsize=10)
arrow(a1, 0.65, 0.75, 1.05, -0.1); arrow(a1, 0.5, -1.05, -0.5, -1.05); arrow(a1, -1.05, -0.1, -0.65, 0.75)
a1.text(0, -2.05, "16 million ticks every second on an Uno", ha="center", fontsize=11)
a1.set_xlim(-2.1, 2.1); a1.set_ylim(-2.3, 2.1); a1.set_aspect("equal"); a1.axis("off")
a1.set_title("The cycle every CPU repeats", fontsize=13)
prog = [("LOAD", 1), ("OUT", 0), ("WAIT", 500), ("LOAD", 0), ("OUT", 0), ("WAIT", 500), ("JMP", 0)]
codes = {"LOAD": 1, "OUT": 4, "WAIT": 7, "JMP": 5}
for k, (name, arg) in enumerate(prog):
    y = 6 - k
    a2.add_patch(Rectangle((1.2, y), 1.0, 0.8, fc=L_BLUE, ec=BLACK)); a2.text(1.7, y + 0.4, str(codes[name]), ha="center", va="center")
    a2.add_patch(Rectangle((2.2, y), 1.0, 0.8, fc=L_BLUE, ec=BLACK)); a2.text(2.7, y + 0.4, str(arg), ha="center", va="center")
    a2.text(0.9, y + 0.4, f"{k}", ha="right", va="center", fontsize=11)
    a2.text(3.5, y + 0.4, f"{name} {arg if name != 'OUT' else ''}", va="center", fontsize=12, family="monospace")
a2.text(1.7, 7.1, "flash: just numbers", ha="left", fontsize=11)
a2.text(0.4, 7.1, "address", ha="left", fontsize=10)
arrow(a2, -0.4, 4.4, 0.45, 4.4, color=RED, lw=2.5)
a2.text(-0.45, 4.4, "pc = 2", ha="right", va="center", color=RED, fontsize=12, weight="bold")
a2.text(3.5, -0.6, "JMP 0 sends pc back to the top: blink for ever", fontsize=11)
a2.set_xlim(-2.0, 7.4); a2.set_ylim(-1.0, 7.6); a2.axis("off")
a2.set_title("The program counter (pc) points at the next instruction", fontsize=13)
save(fig, "fig03-fetch-execute.png")

# Figure 4: three kinds of memory
fig, ax = plt.subplots(figsize=(11, 5.4))
cols = [("FLASH", "like a printed book", L_BLUE, ["Uno: 32,768 bytes", "holds: the program", "power off: KEPT",
                                                     "written: when you upload", "wears out after: ~10,000 writes"]),
        ("SRAM", "like a whiteboard", L_GREEN, ["Uno: 2,048 bytes", "holds: variables", "power off: LOST",
                                                 "written: all the time", "wears out: never"]),
        ("EEPROM", "like a small notebook", L_GREY, ["Uno: 1,024 bytes", "holds: saved settings", "power off: KEPT",
                                                      "written: by your program, rarely", "wears out after: ~100,000 writes"])]
for k, (name, like, col, lines) in enumerate(cols):
    x = k * 3.85
    box(ax, x, 0, 3.65, 4.6, "", col)
    ax.text(x + 1.82, 4.15, name, ha="center", fontsize=15, weight="bold")
    ax.text(x + 1.82, 3.7, like, ha="center", fontsize=11, style="italic")
    for j, t in enumerate(lines):
        c = RED if "LOST" in t else BLACK
        ax.text(x + 0.15, 3.05 - j * 0.62, t, fontsize=10.5, color=c)
ax.set_xlim(-0.2, 11.6); ax.set_ylim(-0.2, 4.8); ax.axis("off")
save(fig, "fig04-three-memories.png")

# Figure 5: the cycle budget (from cycle_budget.py)
ops = ["int add", "int multiply", "float add", "float multiply", "float divide", "sin()"]
uno = [8000, 1600, 160, 106, 32, 9]
stm = [168000, 168000, 168000, 168000, 12000, 2100]
fig, ax = plt.subplots(figsize=(11, 5))
ys = range(len(ops))
ax.barh([y + 0.2 for y in ys], uno, height=0.38, color=ORANGE, label="Uno (AVR, 16 MHz, no float hardware)")
ax.barh([y - 0.2 for y in ys], stm, height=0.38, color=BLUE, label="STM32F4 (168 MHz, with float hardware)", hatch="//", ec="white")
for y, u in zip(ys, uno):
    ax.text(u * 1.15, y + 0.2, f"{u:,}", va="center", fontsize=11)
ax.set_yticks(list(ys)); ax.set_yticklabels(ops); ax.invert_yaxis()
ax.set_xscale("log"); ax.set_xticks([1, 10, 100, 1000, 10000, 100000, 1000000])
ax.set_xticklabels(["1", "10", "100", "1,000", "10,000", "100,000", "1,000,000"]); ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xlim(1, 3e6)
ax.set_xlabel("how many fit in one 1 ms loop (log scale)")
ax.legend(loc="lower right", fontsize=11); ax.grid(axis="x", alpha=0.3)
save(fig, "fig05-cycle-budget.png")

# Figure 6: microcontrollers and a computer, side by side (log scales)
names = ["ATmega328P\n(Arduino Uno)", "RP2040\n(Pi Pico)", "STM32F405\n(drone board)", "ESP32", "Raspberry Pi 4\n(a computer)"]
clock = [16, 133, 168, 240, 1500]
ram = [2, 264, 192, 520, 4 * 1024 * 1024]          # KB
power = [0.05, 0.1, 0.2, 0.5, 4.0]                   # W, rough, chip or board running
fig, axes = plt.subplots(1, 3, figsize=(13, 4.8), sharey=True)
colors = [ORANGE, GREEN, GREEN, GREEN, BLUE]
for ax, vals, title, ticks, labels in [
        (axes[0], clock, "clock (MHz)", [10, 100, 1000, 10000], ["10", "100", "1,000", "10,000"]),
        (axes[1], ram, "working memory (KB)", [1, 100, 10000, 1e6, 1e8], ["1", "100", "10 MB", "1 GB", "100 GB"]),
        (axes[2], power, "power while running (W)", [0.01, 0.1, 1, 10], ["0.01", "0.1", "1", "10"])]:
    ax.barh(range(5), vals, color=colors)
    ax.set_xscale("log"); ax.set_xticks(ticks); ax.set_xticklabels(labels); ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(ticks[0] * 0.5, ticks[-1] * 2); ax.set_title(title, fontsize=12); ax.grid(axis="x", alpha=0.3)
axes[0].set_yticks(range(5)); axes[0].set_yticklabels(names, fontsize=10); axes[0].invert_yaxis()
for k, v in enumerate(ram):
    axes[1].text(v * 1.4, k, "4 GB" if k == 4 else f"{v} KB", va="center", fontsize=10)
fig.suptitle("Microcontrollers (orange, green) and a small computer (blue): rough numbers", fontsize=13)
fig.tight_layout()
save(fig, "fig06-mcu-vs-computer.png")

# Figure 7: loop timing - the same model as jitter_compare.py
random.seed(94)
mcu = [abs(random.gauss(0, 0.002)) for _ in range(10_000)]
lin = []
for _ in range(10_000):
    late = abs(random.gauss(0, 0.05))
    if random.random() < 0.01:
        late += random.uniform(1, 20)
    lin.append(late)
fig, axes = plt.subplots(2, 1, figsize=(11, 5.6), sharex=True)
t = [k / 100 for k in range(10_000)]
axes[0].plot(t, mcu, color=ORANGE, lw=2); axes[0].set_ylim(0, 22); axes[0].text(50, 6, "the orange line sits on the bottom, at about 0.002 ms: too small to see on this scale", ha="center", fontsize=11, color=ORANGE)
axes[0].set_title("microcontroller: every loop starts within a few microseconds", fontsize=12)
axes[1].plot(t, lin, color=BLUE, lw=1); axes[1].set_ylim(0, 22)
axes[1].set_title("Linux computer: usually on time, but about 1 loop in 100 is late by 1-20 ms", fontsize=12)
for ax in axes:
    ax.set_ylabel("late (ms)"); ax.grid(alpha=0.3)
axes[1].set_xlabel("time (s) - 10,000 loops of a 100 Hz control loop (a model)")
fig.tight_layout()
save(fig, "fig07-loop-timing.png")

# Figure 8: Rover's two brains
fig, ax = plt.subplots(figsize=(11, 5.6))
box(ax, 0.2, 1.4, 3.6, 2.6, "", L_ORANGE)
ax.text(2.0, 3.6, "Arduino Uno", ha="center", fontsize=14, weight="bold")
ax.text(2.0, 3.2, "fast, exact, simple jobs", ha="center", fontsize=11, style="italic")
for j, t in enumerate(["count encoder pulses", "wheel speed control 100 Hz", "bumpers, line sensors",
                       "ultrasonic distance", "stop at once if bumped"]):
    ax.text(0.4, 2.75 - j * 0.3, "- " + t, fontsize=11)
box(ax, 6.6, 1.4, 3.6, 2.6, "", L_BLUE)
ax.text(8.4, 3.6, "Raspberry Pi", ha="center", fontsize=14, weight="bold")
ax.text(8.4, 3.2, "big, slow-to-start, clever jobs", ha="center", fontsize=11, style="italic")
for j, t in enumerate(["camera: find the ball", "maps (SLAM)", "plan a path", "Wi-Fi, logs, ROS 2"]):
    ax.text(6.8, 2.75 - j * 0.3, "- " + t, fontsize=11)
arrow(ax, 3.9, 2.9, 6.5, 2.9, color=GREEN, lw=2.5)
arrow(ax, 6.5, 2.4, 3.9, 2.4, color=GREEN, lw=2.5)
ax.text(5.2, 3.1, "status: speed, distance", ha="center", fontsize=10)
ax.text(5.2, 2.05, "commands: 'drive 0.3 m/s'", ha="center", fontsize=10)
ax.text(5.2, 1.6, "UART wires (Ch 91)", ha="center", fontsize=10, color=GREEN)
for x, t in [(0.4, "motors"), (1.6, "encoders"), (2.8, "sensors")]:
    box(ax, x, 0.1, 1.0, 0.6, t, L_GREY, fs=10)
    arrow(ax, x + 0.5, 0.75, x + 0.5, 1.35, style="<|-|>")
for x, t in [(6.9, "camera"), (8.9, "LiDAR")]:
    box(ax, x, 0.1, 1.0, 0.6, t, L_GREY, fs=10)
    arrow(ax, x + 0.5, 0.75, x + 0.5, 1.35, style="<|-|>")
ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.2); ax.axis("off")
save(fig, "fig08-rover-brains.png")
print("figures saved in", os.path.abspath(OUT))
