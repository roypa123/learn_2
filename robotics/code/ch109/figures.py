# Figures for Chapter 109 - Communication part 3: SPI.
# Run:  python figures.py      (saves PNG files in ../../images/ch109/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch109")
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


def arrow(ax, a, b, col=BLACK):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=1.6, color=col))


# Figure 1: SPI wiring: shared SCK, MOSI, MISO; one chip-select per target
fig, ax = plt.subplots(figsize=(12, 5.0))
box(ax, 0.0, 0.6, 2.6, 4.0, "", L_BLUE); ax.text(1.3, 4.25, "Arduino Uno\ncontroller", ha="center", va="center", fontsize=11)
rows = [(3.4, "SCK (13)", ORANGE), (2.8, "MOSI (11)", BLUE), (2.2, "MISO (12)", GREEN), (1.5, "CS1 (10)", RED), (0.9, "CS2 (9)", RED)]
for y, name, col in rows:
    ax.text(2.5, y, name, ha="right", va="center", fontsize=10)
for k, (x, title) in enumerate([(6.0, "target 1 (IMU)"), (9.4, "target 2 (74HC595)")]):
    box(ax, x, 0.6, 2.4, 3.2, "", L_GREEN if k == 0 else L_ORANGE, 11)
    ax.text(x + 1.2, 0.95, title, ha="center", va="center", fontsize=10.5)
for y, col in [(3.4, ORANGE), (2.8, BLUE)]:
    ax.plot([2.6, 9.4], [y, y], color=col, lw=2)
    for x in (6.0, 9.4):
        ax.plot([x], [y], "o", color=col, ms=6)
ax.plot([2.6, 9.4], [2.2, 2.2], color=GREEN, lw=2)
for x in (6.0, 9.4):
    ax.plot([x], [2.2], "o", color=GREEN, ms=6)
arrow(ax, (3.6, 3.55), (4.4, 3.55), ORANGE); ax.text(4.0, 3.62, "clock", ha="center", fontsize=9, color=ORANGE)
arrow(ax, (3.6, 2.95), (4.4, 2.95), BLUE); ax.text(4.0, 3.02, "data out", ha="center", fontsize=9, color=BLUE)
arrow(ax, (4.4, 2.35), (3.6, 2.35), GREEN); ax.text(4.0, 2.42, "data in", ha="center", fontsize=9, color=GREEN)
ax.plot([2.6, 6.0], [1.5, 1.5], color=RED, lw=2); ax.plot([6.0], [1.5], "o", color=RED, ms=6)
ax.plot([2.6, 5.2, 5.2, 8.8, 8.8, 9.4], [0.9, 0.9, 0.3, 0.3, 1.5, 1.5], color=RED, lw=2); ax.plot([9.4], [1.5], "o", color=RED, ms=6)
ax.text(6.1, 1.5, " CS", va="center", fontsize=9.5); ax.text(9.5, 1.5, " RCLK", va="center", fontsize=9.5)
ax.set_xlim(-0.2, 12.2); ax.set_ylim(0.1, 4.8); ax.axis("off")
save(fig, "fig01-wiring.png")

# Figure 2: the ring of two shift registers
fig, ax = plt.subplots(figsize=(12, 3.8))
for k, b in enumerate(f"{0xA5:08b}"):
    ax.add_patch(Rectangle((0.4 + k * 0.55, 1.6), 0.55, 0.7, fc=L_BLUE, ec=BLACK)); ax.text(0.675 + k * 0.55, 1.95, b, ha="center", va="center")
for k, b in enumerate(f"{0x3C:08b}"):
    ax.add_patch(Rectangle((7.0 + k * 0.55, 1.6), 0.55, 0.7, fc=L_GREEN, ec=BLACK)); ax.text(7.275 + k * 0.55, 1.95, b, ha="center", va="center")
ax.text(2.6, 2.6, "controller's register (0xA5)", ha="center", fontsize=10.5)
ax.text(9.2, 2.6, "target's register (0x3C)", ha="center", fontsize=10.5)
ax.add_patch(FancyArrowPatch((0.45, 2.3), (11.35, 2.3), connectionstyle="arc3,rad=-0.25", arrowstyle="-|>", mutation_scale=14, lw=1.8, color=BLUE))
ax.text(5.9, 4.05, "MOSI: the controller's top bit goes into the target's bottom", ha="center", fontsize=10, color=BLUE)
ax.add_patch(FancyArrowPatch((7.05, 1.6), (4.8, 1.75), connectionstyle="arc3,rad=-0.6", arrowstyle="-|>", mutation_scale=14, lw=1.8, color=GREEN))
ax.text(5.9, 0.25, "MISO: the target's top bit goes into the controller's bottom", ha="center", fontsize=10, color=GREEN)
ax.text(5.9, 1.95, "8 clock\npulses", ha="center", va="center", fontsize=10, color=ORANGE)
ax.set_xlim(0, 11.8); ax.set_ylim(0, 4.3); ax.axis("off")
save(fig, "fig02-ring.png")

# Figure 3: one byte in SPI mode 0: CS, SCK, MOSI (0xA5), MISO (0x3C)
fig, axes = plt.subplots(4, 1, figsize=(12, 5.4), sharex=True)
T = 1.0
t0 = 1.0
cs_x = [0, t0 - 0.5, t0 - 0.5, t0 + 8 * T + 0.5, t0 + 8 * T + 0.5, 10.5]; cs_y = [1, 1, 0, 0, 1, 1]
sck_x, sck_y = [0], [0]
for k in range(8):
    x = t0 + k * T
    sck_x += [x, x, x + T / 2, x + T / 2]; sck_y += [0, 0, 0, 1]
    sck_x += [x + T, x + T]; sck_y += [1, 0]
sck_x += [10.5]; sck_y += [0]


def data_wave(byte):
    xs, ys = [0, t0 - 0.2], [1, 1]
    for k in range(8):
        b = (byte >> (7 - k)) & 1
        xs += [t0 + k * T - 0.2 if k else t0 - 0.2, t0 + (k + 1) * T - 0.2]; ys += [b, b]
    xs += [10.5]; ys += [ys[-1]]
    return xs, ys


for ax, (x, y, name, col) in zip(axes, [(cs_x, cs_y, "CS", RED), (sck_x, sck_y, "SCK", ORANGE),
                                         (*data_wave(0xA5), "MOSI", BLUE), (*data_wave(0x3C), "MISO", GREEN)]):
    ax.plot(x, y, color=col, lw=2, drawstyle="default")
    ax.set_yticks([0, 1]); ax.set_yticklabels(["L", "H"]); ax.set_ylabel(name, rotation=0, labelpad=25)
    ax.set_ylim(-0.25, 1.35)
for k in range(8):
    for ax in axes[1:]:
        ax.axvline(t0 + k * T + T / 2, color=GREY, ls=":", lw=1)
    axes[2].text(t0 + k * T + 0.3, 1.12, str((0xA5 >> (7 - k)) & 1), ha="center", fontsize=10)
    axes[3].text(t0 + k * T + 0.3, 1.12, str((0x3C >> (7 - k)) & 1), ha="center", fontsize=10)
axes[0].text(t0 + 4, 0.35, "LOW: this chip is selected", ha="center", fontsize=10)
axes[3].set_xticks([]); axes[3].set_xlabel("each dotted line is a rising clock edge: both sides read the other's bit there")
save(fig, "fig03-mode0.png")

# Figure 4: inside the 74HC595
fig, ax = plt.subplots(figsize=(12, 4.6))
for k in range(8):
    ax.add_patch(Rectangle((2.0 + k * 0.9, 2.4), 0.9, 0.7, fc=L_BLUE, ec=BLACK)); ax.text(2.45 + k * 0.9, 2.75, f"S{k}", ha="center", va="center", fontsize=10)
    ax.add_patch(Rectangle((2.0 + k * 0.9, 1.0), 0.9, 0.7, fc=L_GREEN, ec=BLACK)); ax.text(2.45 + k * 0.9, 1.35, f"Q{k}", ha="center", va="center", fontsize=10)
    arrow(ax, (2.45 + k * 0.9, 2.4), (2.45 + k * 0.9, 1.72), GREY)
    ax.plot([2.45 + k * 0.9, 2.45 + k * 0.9], [1.0, 0.45], color=ORANGE, lw=2)
    ax.plot([2.45 + k * 0.9], [0.4], "o", color=ORANGE, ms=8)
arrow(ax, (0.6, 2.75), (2.0, 2.75), BLUE); ax.text(0.5, 2.75, "SER\n(data)", ha="right", va="center", fontsize=10)
ax.text(5.6, 3.3, "shift register: at each SRCLK rise, every bit moves one place right, and SER enters at S0", ha="center", fontsize=10)
ax.text(10.5, 1.95, "RCLK rise:\ncopy all 8\ndown at once", va="center", fontsize=10)
arrow(ax, (9.2, 2.75), (10.4, 2.75), BLUE); ax.text(10.5, 2.75, "Q7' (to a second\n595, for 16 outputs)", va="center", fontsize=9.5)
ax.text(5.6, 0.05, "outputs Q0 to Q7: 8 LEDs (or anything else), all changing together", ha="center", fontsize=10)
ax.text(0.5, 1.35, "output\nlatch", ha="right", va="center", fontsize=10)
ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.15, 3.6); ax.axis("off")
save(fig, "fig04-595.png")

# Figure 5: battery voltage and the LED bar (PC test bench)
ts = list(range(1, 12))
volts = [8.09, 7.89, 7.69, 7.50, 7.30, 7.10, 6.90, 6.69, 6.49, 6.29, 6.09]
leds = [7, 6, 6, 5, 4, 4, 3, 2, 2, 1, 0]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5.4), sharex=True, gridspec_kw={"height_ratios": [1.3, 1]})
ax1.plot(ts, volts, "o-", color=BLUE); ax1.set_ylabel("battery (V)"); ax1.grid(alpha=0.3)
ax1.axhline(8.4, color=GREEN, ls="--"); ax1.text(1, 8.25, "full 8.4 V", color=GREEN, fontsize=10)
ax1.axhline(6.0, color=RED, ls="--"); ax1.text(1, 6.1, "empty 6.0 V", color=RED, fontsize=10)
for t, n in zip(ts, leds):
    for k in range(8):
        ax2.add_patch(Rectangle((t - 0.3, k * 0.9), 0.6, 0.75, fc=ORANGE if k < n else "white", ec=GREY))
ax2.set_ylim(-0.2, 7.4); ax2.set_yticks([0.4, 6.7]); ax2.set_yticklabels(["Q0", "Q7"]); ax2.set_xlabel("time (s)")
ax2.set_xlim(0.3, 11.7)
save(fig, "fig05-battery-bar.png")

# Figure 6: time to read the IMU's 14 bytes
names = ["I2C\n100 kHz", "I2C\n400 kHz", "SPI\n1 MHz", "SPI\n8 MHz", "SPI 8 MHz\non the bench\n(with the code's\nown time)"]
times = [1570, 392.5, 120, 15, 38]
fig, ax = plt.subplots(figsize=(10, 4.6))
bars = ax.bar(names, times, color=[ORANGE, ORANGE, BLUE, BLUE, GREEN])
for b, v in zip(bars, times):
    ax.text(b.get_x() + b.get_width() / 2, v * 1.15, f"{v:g} us", ha="center", fontsize=10.5)
ax.set_yscale("log"); ax.set_ylabel("time for one reading (us, log scale)"); ax.set_ylim(5, 5000)
ax.set_yticks([10, 100, 1000]); ax.set_yticklabels(["10", "100", "1000"]); ax.minorticks_off()
save(fig, "fig06-bus-times.png")
print("figures saved in", os.path.abspath(OUT))
