# Figures for Chapter 38 - Powers, roots and scientific notation.
# Run:  python figures.py      (saves PNG files in ../../images/ch038/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch038")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: squares as real shapes
fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
for ax, n in zip(axes, (2, 3, 4)):
    for x in range(n):
        for y in range(n):
            ax.add_patch(Rectangle((x, y), 1, 1, fc=L_BLUE, ec=BLACK, lw=1.3))
    ax.set_title(f"{n} squared = {n} x {n} = {n * n}", fontsize=14)
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(-0.2, 4.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-squares.png")

# Figure 2: ADC staircases
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
v = np.linspace(0, 5, 1000)
for ax, bits in zip(axes, (2, 4)):
    levels = 2 ** bits
    step = 5 / levels
    out = np.floor(np.minimum(v / step, levels - 1)) * step
    ax.plot(v, v, color=BLACK, ls="--", lw=2, label="true voltage")
    ax.plot(v, out, color=BLUE, lw=2.5, label="what the computer stores")
    ax.set_title(f"{bits} bits: 2 to the power {bits} = {levels} levels", fontsize=13.5)
    ax.set_xlabel("true voltage (V)"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
axes[0].set_ylabel("stored voltage (V)")
save(fig, "fig02-adc-steps.png")

# Figure 3: Heron convergence
guess = 6.5
gs = [guess]
for _ in range(6):
    guess = (guess + 13 / guess) / 2
    gs.append(guess)
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.axhline(math.sqrt(13), color=BLACK, ls="--", lw=2, label="true value, 3.6056")
ax.plot(range(7), gs, "o-", color=BLUE, lw=2.5, ms=9, label="our guess")
for i, g in enumerate(gs[:4]):
    ax.annotate(f"{g:.4f}", (i, g), textcoords="offset points", xytext=(8, 8), color=BLUE, fontsize=12)
ax.set_xlabel("step number (0 is the first guess)"); ax.set_ylabel("guess for the square root of 13")
ax.set_ylim(3, 7.2); ax.grid(alpha=0.3); ax.legend()
save(fig, "fig03-heron.png")

# Figure 4: scale ladder
rows = [("giga", "1e9", "billion"), ("mega", "1e6", "million"), ("kilo", "1e3", "thousand"),
        ("(none)", "1", "one"), ("milli", "1e-3", "thousandth"), ("micro", "1e-6", "millionth"), ("nano", "1e-9", "billionth")]
examples = ["1 GHz: a fast computer clock", "1 MB: about a million bytes", "1 km: a long robot trip", "1 m: a short Rover trip",
            "1 ms: a fast control step", "1 us: a fast sensor pulse", "6.67 ns: laser round trip to 1 m"]
fig, ax = plt.subplots(figsize=(12, 5.4))
for i, (r, ex) in enumerate(zip(rows, examples)):
    y = 6 - i
    ax.add_patch(Rectangle((0, y), 11.8, 0.86, fc=(L_ORANGE if i == 3 else (L_BLUE if i < 3 else L_GREEN)), ec=BLACK))
    ax.text(0.2, y + 0.43, r[0], va="center", fontsize=13, weight="bold")
    ax.text(2.1, y + 0.43, r[1], va="center", fontsize=13, family="DejaVu Sans Mono")
    ax.text(3.6, y + 0.43, r[2], va="center", fontsize=13)
    ax.text(6.0, y + 0.43, ex, va="center", fontsize=12.5)
ax.set_xlim(-0.05, 11.9); ax.set_ylim(-0.05, 7); ax.axis("off")
save(fig, "fig04-prefix-ladder.png")

# Figure 5: thrust against rpm
K = 4.08e-8
rpm = np.linspace(0, 14000, 300)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(rpm, K * rpm ** 2, color=BLUE, lw=3, label="thrust = K x rpm squared")
hover = math.sqrt(1.6 * 9.81 / 4 / K)
ax.axhline(1.6 * 9.81 / 4, color=BLACK, ls="--", lw=2, label="thrust needed to hover (3.92 N)")
ax.plot([hover], [3.924], "o", color=ORANGE, mec=BLACK, ms=12, zorder=5)
ax.annotate(f"hover at {hover:.0f} rpm", (hover, 3.924), xytext=(4300, 5.4), fontsize=12.5, arrowprops=dict(arrowstyle="-|>", color=BLACK))
ax.set_xlabel("motor speed (rpm)"); ax.set_ylabel("thrust of one motor (N)"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
ax.set_xlim(0, 14000); ax.set_ylim(0, 8.5)
save(fig, "fig05-thrust-rpm.png")
print("figures saved in", os.path.abspath(OUT))
