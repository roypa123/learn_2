# Figures for Chapter 73 - What is electricity? Charge and electrons.
# Run:  python figures.py      (saves PNG files in ../../images/ch073/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch073")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def circle(ax, x, y, r, color, text="", tc=BLACK, fs=11, ec=BLACK):
    ax.add_patch(plt.Circle((x, y), r, color=color, ec=ec, zorder=3))
    if text:
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, color=tc, zorder=4, fontweight="bold")


# Figure 1: a copper atom (simplified) with its nucleus and electron shells
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_aspect("equal"); ax.axis("off")
cx, cy = 0, 0
circle(ax, cx, cy, 0.55, L_ORANGE, "nucleus\n29 protons (+)\n35 neutrons", fs=10.5)
for r, n in [(1.3, 2), (1.9, 8), (2.5, 18), (3.1, 1)]:
    ax.add_patch(plt.Circle((cx, cy), r, fill=False, ec=GREY, ls="--", lw=1.2))
    for k in range(n):
        a = 2 * math.pi * k / n + (0.3 if n == 1 else 0) + (math.pi / 2 if n == 2 else 0)
        circle(ax, cx + r * math.cos(a), cy + r * math.sin(a), 0.11, BLUE, "-", tc="white", fs=9)
ax.annotate("the outer electron is held weakly:\nit can wander off to other atoms\n(a 'free electron')", xy=(3.1 * math.cos(0.3), 3.1 * math.sin(0.3)),
            xytext=(3.4, 1.9), fontsize=10.5, arrowprops=dict(arrowstyle="->", color=BLACK))
ax.text(0, -3.65, "a copper atom: 29 electrons (-) around 29 protons (+), so the whole atom is neutral",
        ha="center", fontsize=11)
ax.text(3.6, -1.2, "electron: charge -1.602 x 10^-19 C\nproton:  charge +1.602 x 10^-19 C\nneutron: no charge", fontsize=10.5,
        bbox=dict(boxstyle="round", fc="white", ec=GREY))
ax.set_xlim(-3.8, 6.4); ax.set_ylim(-3.9, 3.6)
save(fig, "fig01-atom.png")

# Figure 2: like charges push apart, opposite charges pull together
fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
for ax, (a, b, title, dirs) in zip(axes, [("+", "+", "two positive: push apart", (-1, 1)),
                                           ("-", "-", "two negative: push apart", (-1, 1)),
                                           ("+", "-", "positive and negative: pull together", (1, -1))]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.3, 1.3)
    circle(ax, -1, 0, 0.42, RED if a == "+" else BLUE, a, tc="white", fs=16)
    circle(ax, 1, 0, 0.42, RED if b == "+" else BLUE, b, tc="white", fs=16)
    for x, d in zip([-1, 1], dirs):
        ax.annotate("", xy=(x + 1.1 * d, 0), xytext=(x + 0.5 * d, 0), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=BLACK))
    ax.set_title(title, fontsize=11.5)
save(fig, "fig02-push-pull.png")

# Figure 3: conductor vs insulator
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
rng = np.random.default_rng(3)
for ax, kind in zip(axes, ["conductor (copper)", "insulator (plastic)"]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 7.5); ax.set_ylim(-0.6, 4.6)
    ax.add_patch(plt.Rectangle((0, 0), 7, 4, color=L_ORANGE if kind.startswith("c") else L_GREY, ec=BLACK))
    for i in range(7):
        for j in range(4):
            circle(ax, i + 0.5, j + 0.5, 0.2, ORANGE if kind.startswith("c") else GREY, "+", tc="white", fs=8)
            if kind.startswith("i"):
                circle(ax, i + 0.5 + 0.28, j + 0.5 + 0.22, 0.1, BLUE)
    if kind.startswith("c"):
        for k in range(26):
            x, y = rng.uniform(0.2, 6.8), rng.uniform(0.2, 3.8)
            circle(ax, x, y, 0.1, BLUE)
            ax.annotate("", xy=(x + rng.uniform(-0.4, 0.4), y + rng.uniform(-0.4, 0.4)), xytext=(x, y),
                        arrowprops=dict(arrowstyle="->", color=BLUE, lw=1))
        ax.set_title("conductor (copper): free electrons wander\nbetween the atoms, so charge can flow", fontsize=11)
    else:
        ax.set_title("insulator (plastic): every electron stays\nwith its own atom, so nothing flows", fontsize=11)
save(fig, "fig03-conductor-insulator.png")

# Figure 4: current = charge passing a gate each second
fig, ax = plt.subplots(figsize=(11, 4))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 11.5); ax.set_ylim(-2.2, 2.4)
ax.add_patch(plt.Rectangle((0, -0.6), 11, 1.2, color=L_ORANGE, ec=BLACK))
rng = np.random.default_rng(5)
for k in range(40):
    x, y = rng.uniform(0.2, 10.8), rng.uniform(-0.42, 0.42)
    circle(ax, x, y, 0.09, BLUE)
ax.plot([5.5, 5.5], [-0.9, 0.9], color=RED, lw=3, ls="--")
ax.text(5.5, 1.1, "counting gate", color=RED, ha="center", fontsize=11.5)
ax.annotate("", xy=(9.5, 1.6), xytext=(7.0, 1.6), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=BLUE))
ax.text(8.25, 1.85, "electrons drift this way", ha="center", color=BLUE, fontsize=11)
ax.annotate("", xy=(2.0, 1.6), xytext=(4.5, 1.6), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=RED))
ax.text(3.25, 1.85, "'conventional current' arrow", ha="center", color=RED, fontsize=11)
ax.text(5.5, -1.35, "current I = charge that passes the gate each second\n1 ampere = 1 coulomb per second = 6.24 x 10^18 electrons per second",
        ha="center", fontsize=11.5)
save(fig, "fig04-current-gate.png")

# Figure 5: a pipe full of marbles: push one in, one comes out at once
fig, axes = plt.subplots(2, 1, figsize=(11, 4.4))
for ax, (title, shift) in zip(axes, [("before the push", 0), ("just after one push from the left", 0.55)]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 12.5); ax.set_ylim(-1.0, 1.2)
    ax.add_patch(plt.Rectangle((0, -0.5), 11, 1.0, fill=False, ec=BLACK, lw=2))
    for k in range(20):
        circle(ax, 0.3 + k * 0.55 + shift, 0, 0.25, BLUE if (k, shift) != (0, 0.55) else GREEN, ec=BLACK)
    if shift:
        ax.annotate("", xy=(0.0, 0), xytext=(-1.2, 0), arrowprops=dict(arrowstyle="-|>", lw=3, color=GREEN))
        ax.annotate("", xy=(12.3, 0), xytext=(11.3, 0), arrowprops=dict(arrowstyle="-|>", lw=3, color=BLUE))
        ax.text(11.8, 0.6, "one pops out\nat once", ha="center", fontsize=10.5)
    ax.set_title(title, fontsize=11.5, loc="left")
fig.suptitle("each marble moves only a little, but the message 'push' travels the whole pipe instantly", fontsize=12, y=0.02)
save(fig, "fig05-marble-pipe.png")

# Figure 6: a closed loop and an open loop, with the water picture
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
for ax, closed in zip(axes, [True, False]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.8, 6.8); ax.set_ylim(-0.8, 4.8)
    # battery
    ax.add_patch(plt.Rectangle((0, 1.2), 1.0, 1.8, color=ORANGE, ec=BLACK))
    ax.text(0.5, 2.1, "battery\n(pump)", ha="center", va="center", fontsize=10)
    ax.text(1.25, 2.85, "+", fontsize=14, fontweight="bold"); ax.text(1.25, 1.05, "-", fontsize=16, fontweight="bold")
    # bulb
    ax.add_patch(plt.Circle((5.5, 2.1), 0.6, color=L_ORANGE if closed else "white", ec=BLACK, lw=2))
    ax.text(5.5, 2.1, "lamp", ha="center", va="center", fontsize=10)
    # wires
    ax.plot([0.5, 0.5, 5.5, 5.5], [3.0, 4.2, 4.2, 2.7], color=BLACK, lw=2.5)
    if closed:
        ax.plot([0.5, 0.5, 5.5, 5.5], [1.2, 0.0, 0.0, 1.5], color=BLACK, lw=2.5)
        for (x, y, dx, dy) in [(2.5, 4.2, 1, 0), (5.5, 0.9, 0, 0.0), (3.5, 0.0, -1, 0), (0.5, 2.0, 0, 0)]:
            if dx or dy:
                ax.annotate("", xy=(x + dx * 0.6, y), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", lw=2, color=RED))
        ax.text(3.0, 2.1, "a closed loop:\ncharge flows round\nand the lamp lights", ha="center", fontsize=11)
    else:
        ax.plot([0.5, 0.5, 2.6], [1.2, 0.0, 0.0], color=BLACK, lw=2.5)
        ax.plot([3.6, 5.5, 5.5], [0.0, 0.0, 1.5], color=BLACK, lw=2.5)
        ax.text(3.1, -0.5, "gap", ha="center", color=RED, fontsize=11)
        ax.text(3.0, 2.1, "an open loop:\nnothing flows,\nthe lamp is dark", ha="center", fontsize=11)
save(fig, "fig06-loop.png")
print("saved 6 figures")
