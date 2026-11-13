# Figures for Chapter 106 - Hardware timers.
# Run:  python figures.py      (saves PNG files in ../../images/ch106/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch106")
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


def arrow(ax, a, b):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, lw=1.5))


# Figure 1: the Uno's three timers and what the Arduino core uses them for
fig, ax = plt.subplots(figsize=(12, 4.6))
rows = [("Timer0\n8 bits", L_BLUE, "millis(), micros(), delay()", "PWM on pins 5 and 6 (980 Hz)", "change it and time goes wrong"),
        ("Timer1\n16 bits", L_GREEN, "the Servo library", "PWM on pins 9 and 10 (490 Hz)", "the most precise: free for you"),
        ("Timer2\n8 bits", L_ORANGE, "tone()", "PWM on pins 3 and 11 (490 Hz)", "tone() stops PWM on 3 and 11")]
for k, (name, col, use1, use2, note) in enumerate(rows):
    y = 3.0 - k * 1.3
    box(ax, 0, y, 1.8, 1.0, name, col, 12)
    box(ax, 2.6, y, 3.2, 1.0, use1, "white")
    box(ax, 6.3, y, 4.0, 1.0, use2, "white")
    ax.text(10.6, y + 0.5, note, va="center", fontsize=10.5, color=RED if k != 1 else GREEN)
    arrow(ax, (1.85, y + 0.5), (2.55, y + 0.5))
ax.text(4.2, 4.25, "used by the Arduino core for ...", ha="center", fontsize=11)
ax.text(8.3, 4.25, "... and for analogWrite on", ha="center", fontsize=11)
ax.set_xlim(-0.2, 14.2); ax.set_ylim(0.2, 4.6); ax.axis("off")
save(fig, "fig01-three-timers.png")

# Figure 2: inside a timer: clock -> prescaler -> counter -> compare -> interrupt / pin
fig, ax = plt.subplots(figsize=(12, 3.6))
box(ax, 0.0, 1.2, 1.8, 1.0, "16 MHz\nclock", L_GREY)
box(ax, 2.5, 1.2, 2.0, 1.0, "prescaler\n÷ 1, 8, 64,\n256 or 1024", L_ORANGE, 10.5)
box(ax, 5.2, 1.2, 2.0, 1.0, "counter\nTCNT1\n0, 1, 2, ...", L_BLUE, 10.5)
box(ax, 7.9, 1.2, 2.0, 1.0, "compare:\nTCNT1 ==\nOCR1A ?", L_GREEN, 10.5)
box(ax, 10.6, 2.0, 2.0, 0.8, "interrupt\n(ISR)", "white", 10.5)
box(ax, 10.6, 0.6, 2.0, 0.8, "output pin\n(9 for OCR1A)", "white", 10.5)
for a, b in [((1.8, 1.7), (2.5, 1.7)), ((4.5, 1.7), (5.2, 1.7)), ((7.2, 1.7), (7.9, 1.7)), ((9.9, 1.9), (10.6, 2.4)), ((9.9, 1.5), (10.6, 1.0))]:
    arrow(ax, a, b)
ax.text(2.15, 1.85, "ticks", ha="center", fontsize=9.5); ax.text(4.85, 1.85, "slower", ha="center", fontsize=9.5)
ax.text(8.9, 0.85, "match: start again at 0 (CTC)", ha="center", fontsize=9.5)
ax.set_xlim(-0.2, 12.8); ax.set_ylim(0.4, 3.0); ax.axis("off")
save(fig, "fig02-inside-a-timer.png")

# Figure 4: CTC mode: the count climbs to OCR1A, matches, goes back to 0 (timer1_blink: 2 matches per second)
t = np.linspace(0, 2.0, 4001)
count = ((t * 62500) % 31250)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
ax1.plot(t, count, color=BLUE, lw=2)
ax1.axhline(31249, color=GREEN, ls="--", lw=1.5); ax1.text(0.02, 32200, "OCR1A = 31249", color=GREEN, fontsize=10.5)
for m in [0.5, 1.0, 1.5, 2.0]:
    ax1.plot([m], [31249], "o", color=RED, ms=8)
ax1.text(0.52, 25000, "match: the ISR runs\nand TCNT1 goes back to 0", color=RED, fontsize=10)
ax1.set_ylabel("TCNT1"); ax1.set_ylim(0, 36000); ax1.grid(alpha=0.3)
led = (np.floor(t / 0.5) % 2)
ax2.plot(t, led, color=ORANGE, lw=2, drawstyle="steps-post")
ax2.set_yticks([0, 1]); ax2.set_yticklabels(["LOW", "HIGH"]); ax2.set_ylabel("pin 13"); ax2.set_xlabel("time (s)")
ax2.set_ylim(-0.2, 1.2)
save(fig, "fig04-ctc.png")

# Figure 3: the bit operators on a register byte
fig, ax = plt.subplots(figsize=(11, 4.4))
steps = [("reg = 0b00000011", 0b00000011, []),
         ("reg |= (1 << 3)      set bit 3", 0b00001011, [3]),
         ("reg &= ~(1 << 3)     clear bit 3", 0b00000011, [3]),
         ("reg ^= (1 << 5)      toggle bit 5", 0b00100011, [5])]
for r, (label, v, changed) in enumerate(steps):
    y = 3 - r
    ax.text(-0.2, y + 0.4, label, ha="right", va="center", fontsize=11, family="monospace")
    for b in range(8):
        x = 7 - b
        bit = (v >> b) & 1
        col = L_ORANGE if b in changed else (L_BLUE if bit else "white")
        ax.add_patch(Rectangle((x * 0.8, y), 0.75, 0.8, fc=col, ec=BLACK))
        ax.text(x * 0.8 + 0.375, y + 0.4, str(bit), ha="center", va="center", fontsize=13)
for b in range(8):
    ax.text((7 - b) * 0.8 + 0.375, 4.05, f"bit {b}", ha="center", fontsize=9)
ax.set_xlim(-5.6, 6.6); ax.set_ylim(-0.2, 4.4); ax.axis("off")
save(fig, "fig03-bits.png")

# Figure 5: gap between control steps: millis() timing with a slow job vs a timer interrupt
# Gaps (us) between the first 61 steps of tick_millis.ino, logged on the PC test bench;
# tick_timer.ino measured exactly 10,000 us for every gap.
GAPS_US = [10003, 9998, 11003, 8998, 9998, 10003, 9998, 10003, 9998, 11003, 8998, 9998, 16003, 3998, 9998,
           10003, 11003, 8998, 9998, 9998, 10003, 9998, 10003, 11003, 8993, 10003, 9998, 10003, 9998, 9998,
           11008, 8993, 10003, 9998, 9998, 10003, 9998, 11003, 8998, 9998, 10003, 9998, 10003, 9998, 11003,
           8998, 9998, 16003, 3998, 9998, 10003, 11003, 8998, 9998, 9998, 10003, 9998, 10003, 11003, 8993]
gaps_m = np.array(GAPS_US) / 1000
fig, ax = plt.subplots(figsize=(11, 4.4))
ax.plot(range(1, len(gaps_m) + 1), gaps_m, "o-", color=RED, ms=5, label="timed with millis() in loop()")
ax.plot(range(1, len(gaps_m) + 1), [10] * len(gaps_m), "o-", color=GREEN, ms=5, label="started by a Timer1 interrupt")
ax.set_xlabel("control step number"); ax.set_ylabel("gap since the previous step (ms)"); ax.set_ylim(0, 18)
ax.legend(fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig05-step-gaps.png")

# Figure 6: fast PWM with TOP = ICR1 = 799: the count, OCR1A, and pin 9
t = np.linspace(0, 150, 6001)                      # microseconds: three periods of 50 us
cnt = (t * 16) % 800
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 5.2), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
ax1.plot(t, cnt, color=BLUE, lw=2)
ax1.axhline(799, color=GREY, ls=":", lw=1.5); ax1.text(1, 820, "TOP = ICR1 = 799", fontsize=10.5)
ax1.axhline(399, color=GREEN, ls="--", lw=1.5); ax1.text(1, 420, "OCR1A = 399 (50 %)", color=GREEN, fontsize=10.5)
ax1.set_ylabel("TCNT1"); ax1.set_ylim(0, 900); ax1.grid(alpha=0.3)
ax2.plot(t, (cnt <= 399) * 1.0, color=ORANGE, lw=2)
ax2.set_yticks([0, 1]); ax2.set_yticklabels(["LOW", "HIGH"]); ax2.set_ylabel("pin 9"); ax2.set_xlabel("time (us)")
ax2.set_ylim(-0.2, 1.2)
save(fig, "fig06-fast-pwm.png")
print("figures saved in", os.path.abspath(OUT))
