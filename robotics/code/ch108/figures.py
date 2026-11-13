# Figures for Chapter 108 - Communication part 2: I2C.
# Run:  python figures.py      (saves PNG files in ../../images/ch108/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch108")
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


def resistor(ax, x, y0, y1, label):
    ax.plot([x, x], [y0, y0 + 0.25], color=BLACK, lw=1.5)
    ax.add_patch(Rectangle((x - 0.12, y0 + 0.25), 0.24, (y1 - y0) - 0.5, fc="white", ec=BLACK))
    ax.plot([x, x], [y1 - 0.25, y1], color=BLACK, lw=1.5)
    ax.text(x + 0.2, (y0 + y1) / 2, label, va="center", fontsize=9.5)


# Figure 1: the bus: one controller, several targets, two shared wires, two pull-ups
fig, ax = plt.subplots(figsize=(12, 4.8))
ax.plot([0.5, 2.48], [3.0, 3.0], color=BLUE, lw=3); ax.plot([2.72, 11.5], [3.0, 3.0], color=BLUE, lw=3)
hop = np.linspace(0, np.pi, 30)
ax.plot(2.6 - 0.12 * np.cos(hop), 3.0 + 0.12 * np.sin(hop), color=BLUE, lw=3)   # SDA hops over the SCL pull-up wire
ax.text(11.6, 3.0, "SDA (data)", va="center", color=BLUE)
ax.plot([0.5, 11.5], [2.4, 2.4], color=ORANGE, lw=3); ax.text(11.6, 2.4, "SCL (clock)", va="center", color=ORANGE)
ax.plot([0.5, 3.5], [4.4, 4.4], color=RED, lw=2); ax.text(0.5, 4.55, "5 V", color=RED)
resistor(ax, 1.5, 3.0, 4.4, "4.7 k"); resistor(ax, 2.6, 2.4, 4.4, "4.7 k")
ax.plot([2.6, 2.6], [2.4, 3.0], color=BLACK, lw=0)
devices = [(0.6, "Arduino Uno\ncontroller\nA4 = SDA, A5 = SCL", L_BLUE), (4.0, "IMU\nMPU-6050\naddress 0x68", L_GREEN),
           (6.6, "I/O expander\nPCF8574\naddress 0x20", L_GREEN), (9.2, "another chip\nits own\naddress", L_GREY)]
for x, text, col in devices:
    box(ax, x, 0.2, 2.2, 1.4, text, col, 10)
    ax.plot([x + 0.7, x + 0.7], [1.6, 3.0], color=BLUE, lw=1.8)
    ax.plot([x + 1.5, x + 1.5], [1.6, 2.4], color=ORANGE, lw=1.8)
    ax.plot([x + 0.7], [3.0], "o", color=BLUE, ms=6); ax.plot([x + 1.5], [2.4], "o", color=ORANGE, ms=6)
ax.text(6.0, 4.3, "every chip also shares GND (not drawn)", ha="center", fontsize=10)
ax.set_xlim(0, 13.4); ax.set_ylim(0, 4.9); ax.axis("off")
save(fig, "fig01-bus.png")

# Figure 2: open drain: pulled LOW quickly by a transistor, pulled HIGH slowly by the resistor
t = np.linspace(0, 4, 800)                          # microseconds
fig, ax = plt.subplots(figsize=(11, 4.4))
for r_k, col in [(1.5, GREEN), (4.7, BLUE), (10, ORANGE), (22, RED)]:
    tau = r_k * 1e3 * 200e-12 * 1e6                 # in microseconds, with 200 pF
    v = np.where(t < 0.5, 0.0, 5 * (1 - np.exp(-(t - 0.5) / tau)))
    ax.plot(t, v, color=col, lw=2, label=f"pull-up {r_k} k")
ax.axhline(0.7 * 5, color=GREY, ls="--"); ax.text(3.0, 3.6, "a chip reads HIGH above 70 %", fontsize=10)
ax.axvline(1.5, color=GREY, ls=":"); ax.text(1.53, 0.3, "1 us after release:\nthe limit at 100 kHz", fontsize=9.5)
ax.set_xlabel("time (us); the transistor lets go of the line at 0.5 us"); ax.set_ylabel("line voltage (V)")
ax.set_title("the same bus (200 pF) with four pull-up resistors", fontsize=11)
ax.legend(fontsize=10, loc="lower right"); ax.grid(alpha=0.3)
save(fig, "fig02-pullup-rise.png")


# Figure 3: one write transaction on the wires: 0x20 + write, then the byte 0xEF
def bits_of(byte):
    return [(byte >> (7 - k)) & 1 for k in range(8)]   # I2C sends the HIGHEST bit first


seq = [("addr", b) for b in bits_of(0x20 << 1 | 0)] + [("ack", 0)] + [("data", b) for b in bits_of(0xEF)] + [("ack", 0)]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(12.5, 4.6), sharex=True)
T = 1.0
xs_scl, ys_scl, xs_sda, ys_sda = [0, 0.5], [1, 1], [0, 0.25], [1, 1]
xs_sda += [0.25]; ys_sda += [0]                      # START: SDA falls while SCL is HIGH
for k, (kind, b) in enumerate(seq):
    x0 = 0.5 + k * T
    xs_scl += [x0, x0, x0 + T / 2, x0 + T / 2, x0 + T]; ys_scl += [1, 0, 0, 1, 1]
    xs_sda += [x0 + 0.1, x0 + 0.1]; ys_sda += [ys_sda[-1], b]
    col = {"addr": L_BLUE, "data": L_GREEN, "ack": L_ORANGE}[kind]
    a2.axvspan(x0 + 0.1, x0 + T + 0.1, color=col, alpha=0.5, lw=0)
    a2.text(x0 + 0.6, 1.25, str(b), ha="center", fontsize=10)
end = 0.5 + len(seq) * T
xs_scl += [end + 1.6]; ys_scl += [1]                  # SCL stays HIGH; the STOP is SDA rising
xs_sda += [end + 0.1, end + 0.1, end + 1.2, end + 1.2, end + 1.6]; ys_sda += [ys_sda[-1], 0, 0, 1, 1]   # STOP: SDA rises while SCL HIGH
a1.plot(xs_scl, ys_scl, color=ORANGE, lw=2); a1.set_yticks([0, 1]); a1.set_yticklabels(["LOW", "HIGH"]); a1.set_ylabel("SCL")
a2.plot(xs_sda, ys_sda, color=BLUE, lw=2); a2.set_yticks([0, 1]); a2.set_yticklabels(["LOW", "HIGH"]); a2.set_ylabel("SDA")
a2.set_ylim(-0.3, 1.6)
a1.text(0.05, 1.12, "START", fontsize=9.5, color=RED); a1.text(end + 0.5, 1.12, "STOP", fontsize=9.5, color=RED)
a2.text(4.5, -0.25, "address 0x20 (7 bits) + 0 = write", ha="center", fontsize=9.5)
a2.text(9.0, -0.25, "ACK", ha="center", fontsize=9.5)
a2.text(13.5, -0.25, "data 0xEF = 1110 1111", ha="center", fontsize=9.5)
a2.text(18.0, -0.25, "ACK", ha="center", fontsize=9.5)
a2.set_xticks([]); a1.set_ylim(-0.2, 1.35)
save(fig, "fig03-transaction.png")

# Figure 4: reading registers: write the register number, repeated start, read
fig, ax = plt.subplots(figsize=(12.5, 2.8))
cells = [("S", L_GREY, "controller"), ("0x68 + W", L_BLUE, "controller"), ("A", L_ORANGE, "IMU"), ("0x3B", L_BLUE, "controller"),
         ("A", L_ORANGE, "IMU"), ("Sr", L_GREY, "controller"), ("0x68 + R", L_BLUE, "controller"), ("A", L_ORANGE, "IMU"),
         ("X high", L_GREEN, "IMU"), ("A", L_ORANGE, "controller"), ("X low", L_GREEN, "IMU"), ("A", L_ORANGE, "controller"),
         ("...", "white", ""), ("Z low", L_GREEN, "IMU"), ("NA", L_RED, "controller"), ("P", L_GREY, "controller")]
x = 0
for text, col, who in cells:
    w = 1.3 if len(text) > 3 else 0.6
    ax.add_patch(Rectangle((x, 0.8), w, 0.8, fc=col, ec=BLACK))
    ax.text(x + w / 2, 1.2, text, ha="center", va="center", fontsize=10)
    x += w
ax.text(x / 2, 1.95, "S = start, Sr = repeated start, A = acknowledge, NA = not acknowledged (\"no more\"), P = stop",
        ha="center", fontsize=10)
ax.text(x / 2, 0.5, "blue and grey: sent by the Uno;  green: sent by the IMU;  orange: the acknowledge, sent by whichever side is receiving",
        ha="center", fontsize=9.5)
ax.set_xlim(-0.1, x + 0.1); ax.set_ylim(0.3, 2.2); ax.axis("off")
save(fig, "fig04-register-read.png")

# Figure 5: Rover's tilt as it drives onto a ramp (PC test bench readings)
tt = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
tilt = [0.6, -1.1, 1.1, -0.7, 0.1, 8.1, 14.0, 16.1, 14.3, 15.1]
x = np.linspace(0, 2050, 500)
true = np.where(x < 1000, 0, np.where(x < 1400, 15 * (x - 1000) / 400, 15))
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.plot(x, true, color=GREY, ls="--", lw=2, label="the real slope")
ax.plot(tt, tilt, "o-", color=BLUE, ms=7, label="tilt from one IMU reading")
ax.set_xlabel("time (ms)"); ax.set_ylabel("tilt (degrees)"); ax.legend(fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig05-tilt.png")

# Figure 6: the expander's eight pins on Rover
fig, ax = plt.subplots(figsize=(11, 4.0))
box(ax, 3.6, 0.4, 3.0, 3.4, "PCF8574\naddress 0x20", L_GREEN, 12)
pins = [("P0", "left bumper (to GND)", BLUE), ("P1", "right bumper (to GND)", BLUE), ("P2", "free", GREY), ("P3", "free", GREY),
        ("P4", "status LED (LOW = on)", ORANGE), ("P5", "free", GREY), ("P6", "buzzer (LOW = on)", ORANGE), ("P7", "free", GREY)]
for k, (p, use, col) in enumerate(pins):
    y = 3.55 - k * 0.43
    ax.plot([6.6, 7.3], [y, y], color=col, lw=2)
    ax.text(6.5, y, p, ha="right", va="center", fontsize=10)
    ax.text(7.4, y, use, va="center", fontsize=10.5, color=col if col != GREY else BLACK)
ax.text(3.4, 2.72, "SDA", ha="right", fontsize=10, color=BLUE); ax.text(3.4, 2.12, "SCL", ha="right", fontsize=10, color=ORANGE)
ax.plot([1.6, 3.6], [2.65, 2.65], color=BLUE, lw=2); ax.plot([1.6, 3.6], [2.05, 2.05], color=ORANGE, lw=2)
ax.text(1.5, 2.35, "to the\nUno's\nbus", ha="right", va="center", fontsize=10)
ax.text(5.1, 0.1, "inputs: written 1 and read; outputs: written 0 for on", ha="center", fontsize=9.5)
ax.set_xlim(0, 11.5); ax.set_ylim(-0.1, 4.0); ax.axis("off")
save(fig, "fig06-expander.png")
print("figures saved in", os.path.abspath(OUT))
