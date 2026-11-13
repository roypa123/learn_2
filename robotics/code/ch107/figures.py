# Figures for Chapter 107 - Communication part 1: UART.
# Run:  python figures.py      (saves PNG files in ../../images/ch107/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch107")
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
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, lw=1.6, color=col))


def frame(byte):
    return [0] + [(byte >> k) & 1 for k in range(8)] + [1]


# Figure 1: one UART frame: 'A' = 0x41 at 9600 baud
bits = [1, 1] + frame(0x41) + [1, 1]
t_bit = 104.17
fig, ax = plt.subplots(figsize=(12, 3.8))
xs = [(k - 2) * t_bit for k in range(len(bits) + 1)]
ax.step(xs, bits + [bits[-1]], where="post", color=BLUE, lw=2.5)
names = ["start"] + [f"bit {k}" for k in range(8)] + ["stop"]
for k, name in enumerate(names):
    x = k * t_bit
    ax.axvline(x, color=GREY, ls=":", lw=1)
    ax.text(x + t_bit / 2, 1.28, name, ha="center", fontsize=9.5)
    ax.text(x + t_bit / 2, 0.5, str(frame(0x41)[k]), ha="center", fontsize=13, color=RED if k in (0, 9) else BLACK)
ax.axvline(10 * t_bit, color=GREY, ls=":", lw=1)
ax.text(-1.6 * t_bit, 1.05, "idle: HIGH", fontsize=10); ax.text(10.2 * t_bit, 1.05, "idle", fontsize=10)
ax.set_yticks([0, 1]); ax.set_yticklabels(["LOW", "HIGH"]); ax.set_ylim(-0.2, 1.45)
ax.set_xlabel("time (us)"); ax.set_xlim(-2 * t_bit, 12 * t_bit)
ax.set_title("'A' = 0x41 = 0b01000001 is sent lowest bit first: 1 0 0 0 0 0 1 0", fontsize=11)
save(fig, "fig01-frame.png")

# Figure 2: the receiver samples in the middle of each bit; a 6 % fast sender drifts out
fig, axes = plt.subplots(2, 1, figsize=(12, 5.4), sharex=True)
for ax, err, title in [(axes[0], 0.0, "sender's clock exact: every sample lands in the middle of its bit"),
                       (axes[1], 0.06, "sender's clock 6 % fast: the last samples land in the NEXT bit")]:
    stream = frame(ord("A")) + frame(ord("B"))
    edges = [k / (1 + err) for k in range(len(stream) + 1)]
    ax.step(edges, stream + [1], where="post", color=BLUE, lw=2)
    for k in range(10):
        ax.axvspan(k / (1 + err), (k + 1) / (1 + err), color=L_GREY if k % 2 else "white", alpha=0.6, lw=0)
        ax.text((k + 0.5) / (1 + err), 1.22, (["S"] + [str(j) for j in range(8)] + ["P"])[k], ha="center", fontsize=9.5)
    for k in range(9):
        t = k + 1.5
        sent = int(t * (1 + err))
        ok = sent == k + 1
        ax.plot([t], [0.5], "o", color=GREEN if ok else RED, ms=9)
    ax.set_title(title, fontsize=10.5); ax.set_yticks([0, 1]); ax.set_yticklabels(["LOW", "HIGH"]); ax.set_ylim(-0.2, 1.4)
axes[1].set_xlabel("time, in the receiver's bit-times (dots: where the receiver reads)")
axes[1].set_xlim(0, 11)
save(fig, "fig02-sampling.png")

# Figure 3: wiring two UART devices, and the Uno's USB chip on pins 0 and 1
fig, ax = plt.subplots(figsize=(12, 4.6))
box(ax, 0.0, 0.5, 3.0, 3.2, "", L_BLUE)
ax.text(1.5, 3.35, "Arduino Uno", ha="center", fontsize=12)
box(ax, 8.6, 0.5, 3.0, 3.2, "", L_GREEN)
ax.text(10.1, 3.35, "other device\n(GPS, Pi, ...)", ha="center", fontsize=11, va="center")
for y, left, right in [(2.5, "TX (pin 1)", "TX"), (1.7, "RX (pin 0)", "RX"), (0.9, "GND", "GND")]:
    ax.text(2.9, y, left, ha="right", va="center", fontsize=10.5)
    ax.text(8.7, y, right, ha="left", va="center", fontsize=10.5)
arrow(ax, (3.0, 2.5), (8.6, 1.7), RED)
arrow(ax, (8.6, 2.5), (3.0, 1.7), BLUE)
ax.plot([3.0, 8.6], [0.9, 0.9], color=BLACK, lw=2)
ax.text(5.8, 2.55, "each TX goes to the other RX", ha="center", fontsize=10.5)
ax.text(5.8, 0.6, "and the grounds are joined", ha="center", fontsize=10.5)
box(ax, 0.3, -1.4, 2.4, 1.0, "USB chip on the Uno\n(to the computer)", L_ORANGE, 10)
ax.plot([1.5, 1.5], [-0.4, 0.5], color=ORANGE, lw=2, ls="--")
ax.text(1.65, 0.0, "also on pins 0 and 1", fontsize=9.5, color=ORANGE)
ax.set_xlim(-0.3, 12); ax.set_ylim(-1.6, 4.0); ax.axis("off")
save(fig, "fig03-wiring.png")

# Figure 4: the packet
fig, ax = plt.subplots(figsize=(12, 3.0))
cells = [("AA", "START", L_GREY), ("04", "LEN", L_ORANGE), ("4D", "TYPE 'M'", L_ORANGE),
         ("78 00", "left = 120", L_BLUE), ("78 00", "right = 120", L_BLUE), ("41", "CHECKSUM", L_GREEN)]
x = 0
for val, label, col in cells:
    w = 2.2 if " " in val else 1.4
    ax.add_patch(Rectangle((x, 0.6), w, 0.9, fc=col, ec=BLACK))
    ax.text(x + w / 2, 1.05, val, ha="center", va="center", fontsize=14, family="monospace")
    ax.text(x + w / 2, 0.3, label, ha="center", fontsize=10.5)
    x += w
ax.text(x / 2, 1.85, "8 bytes: the motor command 'left 120, right 120'", ha="center", fontsize=11)
ax.text(x / 2, -0.15, "CHECKSUM = (04 + 4D + 78 + 00 + 78 + 00) & FF = 141 & FF = 41", ha="center", fontsize=10.5, family="monospace")
ax.set_xlim(-0.2, x + 0.2); ax.set_ylim(-0.4, 2.1); ax.axis("off")
save(fig, "fig04-packet.png")

# Figure 5: the receiving state machine
fig, ax = plt.subplots(figsize=(12, 4.4))
W = 2.1
states = [("WAIT_START", 0.0), ("READ_LEN", 2.9), ("READ_TYPE", 5.8), ("READ_PAYLOAD", 8.7), ("READ_CHECK", 11.6)]
for name, x in states:
    box(ax, x, 1.5, W, 0.9, name, L_BLUE if name != "WAIT_START" else L_GREY, 10.5)
labels = ["AA", "length\nok", "", "got ==\nlen"]
for k in range(4):
    x0 = states[k][1] + W
    x1 = states[k + 1][1]
    arrow(ax, (x0 + 0.03, 1.95), (x1 - 0.03, 1.95))
    ax.text((x0 + x1) / 2, 2.1, labels[k], ha="center", va="bottom", fontsize=9)


def self_loop(x, text):
    ax.add_patch(FancyArrowPatch((x + 0.55, 2.42), (x + 1.55, 2.42), connectionstyle="arc3,rad=-1.0",
                                 arrowstyle="-|>", mutation_scale=12, lw=1.4))
    ax.text(x + 1.05, 3.05, text, ha="center", fontsize=9)


self_loop(0.0, "any other byte")
self_loop(8.7, "each payload byte")
ax.add_patch(FancyArrowPatch((12.65, 1.48), (1.05, 1.48), connectionstyle="arc3,rad=-0.22", arrowstyle="-|>", mutation_scale=14, lw=1.5))
ax.text(6.85, 0.05, "checksum right: use the packet; wrong: count it as bad. Either way, back to WAIT_START.", ha="center", fontsize=10)
ax.text(3.95, 1.3, "length too big: back to WAIT_START", ha="center", fontsize=8.5, color=RED)
ax.set_xlim(-0.3, 14.0); ax.set_ylim(-0.2, 3.4); ax.axis("off")
save(fig, "fig05-parser.png")

# Figure 6: Rover's Arduino-Pi link with level shifting (Chapter 91)
fig, ax = plt.subplots(figsize=(12, 4.6))
box(ax, 0.0, 0.3, 2.8, 3.4, "", L_BLUE); ax.text(1.4, 3.35, "Arduino Uno\n(5 V)", ha="center", va="center", fontsize=11)
box(ax, 9.2, 0.3, 2.8, 3.4, "", L_GREEN); ax.text(10.6, 3.35, "Raspberry Pi\n(3.3 V)", ha="center", va="center", fontsize=11)
ax.text(2.7, 2.5, "TX (pin 1)", ha="right", va="center", fontsize=10.5)
ax.text(9.3, 2.5, "RX (GPIO 15)", ha="left", va="center", fontsize=10.5)
ax.text(2.7, 1.5, "RX (pin 0)", ha="right", va="center", fontsize=10.5)
ax.text(9.3, 1.5, "TX (GPIO 14)", ha="left", va="center", fontsize=10.5)
ax.text(2.7, 0.6, "GND", ha="right", va="center", fontsize=10.5); ax.text(9.3, 0.6, "GND", ha="left", va="center", fontsize=10.5)
ax.plot([2.8, 4.6], [2.5, 2.5], color=RED, lw=2); ax.add_patch(Rectangle((4.6, 2.35), 0.8, 0.3, fc="white", ec=BLACK))
ax.text(5.0, 2.75, "1 k", ha="center", fontsize=9.5)
ax.plot([5.4, 9.2], [2.5, 2.5], color=RED, lw=2)
ax.plot([6.5, 6.5], [2.5, 2.2], color=BLACK, lw=1.5); ax.add_patch(Rectangle((6.35, 1.85), 0.3, 0.35, fc="white", ec=BLACK))
ax.text(6.8, 2.0, "2 k to GND", fontsize=9.5)
ax.text(7.6, 2.65, "3.33 V", fontsize=10, color=RED)
box(ax, 4.3, 1.25, 1.6, 0.5, "BSS138", L_ORANGE, 9.5)
ax.plot([5.9, 9.2], [1.5, 1.5], color=BLUE, lw=2); ax.plot([2.8, 4.3], [1.5, 1.5], color=BLUE, lw=2)
ax.text(3.0, 1.15, "5 V HIGH", fontsize=9.5, color=BLUE); ax.text(7.6, 1.15, "3.3 V HIGH", fontsize=9.5, color=BLUE)
ax.plot([2.8, 9.2], [0.6, 0.6], color=BLACK, lw=2)
ax.set_xlim(-0.3, 12.6); ax.set_ylim(0.0, 4.0); ax.axis("off")
save(fig, "fig06-pi-link.png")
print("figures saved in", os.path.abspath(OUT))
