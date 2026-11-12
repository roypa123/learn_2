# Figures for Chapter 89 - Batteries: types, capacity, C rating, safety.
# Run:  python figures.py      (saves PNG files in ../../images/ch089/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from lipo_model import ocv, SOC_POINTS, OCV_POINTS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch089")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: chemistries - energy per kg against cycle life
fig, ax = plt.subplots(figsize=(10, 5))
chem = [("alkaline", 110, 1, GREY), ("NiMH", 80, 500, BLUE), ("lead-acid", 35, 300, BLACK),
        ("LiFePO4", 140, 3000, GREEN), ("Li-ion 18650", 240, 800, ORANGE), ("LiPo", 180, 300, RED)]
for name, whkg, cyc, col in chem:
    ax.scatter(cyc, whkg, s=260, color=col, edgecolor=BLACK, zorder=3)
    ax.text(cyc * 1.25, whkg + 6, name, fontsize=11)
ax.set_xscale("log"); ax.set_xlabel("full charge cycles before 80% capacity (log scale)"); ax.set_ylabel("energy per kilogram (Wh/kg)")
ax.set_xticks([1, 10, 100, 1000, 10000]); ax.set_xticklabels(["1", "10", "100", "1,000", "10,000"]); ax.set_xlim(0.5, 20000); ax.set_ylim(0, 280)
ax.grid(alpha=0.3, which="both"); ax.set_title("light (up) or long-lived (right): no chemistry is best at everything", fontsize=11.5)
save(fig, "fig01-chemistries.png")

# Figure 2: resting voltage against state of charge
fig, ax = plt.subplots(figsize=(10, 4.8))
s = np.linspace(0, 1, 300)
ax.plot(s * 100, [ocv(x) for x in s], color=BLUE, lw=2.5, label="lithium cell, resting")
ax.plot(np.array(SOC_POINTS) * 100, OCV_POINTS, "o", color=ORANGE, mec=BLACK, ms=7, label="table points")
ax.axhspan(3.3, 3.0, color="#F5C6B0"); ax.text(50, 3.12, "below 3.3 V: stop (below 3.0 V: damage)", ha="center", fontsize=10.5)
ax.axhline(3.8, color=GREEN, ls="--"); ax.text(2, 3.83, "storage: about 3.8 V", fontsize=10.5, color=GREEN)
ax.axhline(4.2, color=RED, ls=":"); ax.text(2, 4.22, "full: 4.2 V (never more)", fontsize=10.5, color=RED)
ax.set_xlabel("charge left (%)"); ax.set_ylabel("volts per cell"); ax.grid(alpha=0.3); ax.set_ylim(2.9, 4.35); ax.legend(loc="lower right", fontsize=10.5)
ax.set_title("flat in the middle, steep at the ends: the voltage is a poor fuel gauge", fontsize=11.5)
save(fig, "fig02-ocv-curve.png")

# Figure 3: discharge curves at different C rates (constant current, with internal resistance)
fig, ax = plt.subplots(figsize=(10, 4.8))
for c, col, ls in [(0.2, GREEN, "-"), (1, BLUE, "-"), (5, ORANGE, "--"), (20, RED, ":")]:
    i = c * 5.0
    used = np.linspace(0, 1, 300)
    v = np.array([ocv(1 - u) for u in used]) - i * 0.005 * (1 + 1.5 * used ** 4)
    keep = v > 3.0
    ax.plot(used[keep] * 100, v[keep], color=col, lw=2.5, ls=ls, label=f"{c:g}C ({i:g} A)")
ax.axhline(3.3, color=BLACK, ls="--", lw=1); ax.text(2, 3.33, "cut-off 3.3 V", fontsize=10)
ax.set_xlabel("charge used (%)"); ax.set_ylabel("volts per cell, under load"); ax.grid(alpha=0.3); ax.legend(title="current", fontsize=10.5)
ax.set_ylim(2.9, 4.3)
ax.set_title("a 5,000 mAh cell: higher current, lower voltage all the way (sag = I x R)", fontsize=11.5)
save(fig, "fig03-discharge.png")

# Figure 4: CC/CV charge
cap, rcell = 5.0, 0.040
soc, t, phase, ts, cur, vol, socs = 0.10, 0.0, "CC", [], [], [], []
while True:
    if phase == "CC":
        i = 5.0
        if ocv(soc) + i * rcell >= 4.2:
            phase = "CV"
    if phase == "CV":
        i = (4.2 - ocv(soc)) / rcell
        if i <= 0.25:
            break
    soc = min(soc + i / 3600 / cap, 1.0); t += 1
    if int(t) % 20 == 0:
        ts.append(t / 60); cur.append(i); vol.append(ocv(soc) + i * rcell); socs.append(soc * 100)
fig, ax1 = plt.subplots(figsize=(10, 4.8))
ax1.plot(ts, cur, color=RED, lw=2.5, label="current (A)"); ax1.set_ylabel("current (A)", color=RED); ax1.set_ylim(0, 6)
ax2 = ax1.twinx(); ax2.plot(ts, vol, color=BLUE, lw=2.5, label="terminal voltage (V)"); ax2.set_ylabel("cell voltage (V)", color=BLUE); ax2.set_ylim(3.6, 4.3)
ax1.plot(ts, np.array(socs) / 100 * 5, color=GREEN, lw=2, ls="--", label="charge (scaled: 5 = full)")
ccend = next(tt for tt, i in zip(ts, cur) if i < 4.99)
ax1.axvline(ccend, color=GREY, ls=":"); ax1.text(ccend / 2, 5.4, "constant current", ha="center", fontsize=10.5); ax1.text(ccend + 15, 5.4, "constant voltage", ha="center", fontsize=10.5)
ax1.set_xlabel("time (min)"); ax1.grid(alpha=0.3); ax1.legend(loc="center left", fontsize=10)
ax1.set_title("charging a lithium cell: full current until 4.2 V, then hold 4.2 V while the current falls", fontsize=11)
save(fig, "fig04-cc-cv.png")

# Figure 5: coulomb counting vs voltage reading in a flight
plan = [(10, 60), (120, 25), (20, 90), (180, 28), (30, 120)]
soc, used, t = 1.0, 0.0, 0.0
ts, true_s, vguess = [], [], []
for sec, amps in plan:
    for _ in range(int(sec / 0.5)):
        soc -= amps * 0.5 / 3600 / 5.0; t += 0.5
        v = ocv(soc) - amps * 0.005
        ts.append(t); true_s.append(soc * 100); vguess.append(float(np.interp(v, OCV_POINTS, SOC_POINTS)) * 100)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(ts, true_s, color=BLUE, lw=2.5, label="coulomb counting (= the true charge here)")
ax.plot(ts, vguess, color=RED, lw=1.5, label="guess from the loaded voltage")
ax.axhline(20, color=BLACK, ls="--"); ax.text(5, 22, "land at 20% left (the 80% rule)", fontsize=10.5)
ax.set_xlabel("flight time (s)"); ax.set_ylabel("charge left (%)"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10.5); ax.set_ylim(0, 105)
ax.set_title("the voltage jumps with every throttle change; counting the current does not", fontsize=11.5)
save(fig, "fig05-coulomb-count.png")

# Figure 6: capacity fade with cycles, and the effect of cold
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
n = np.arange(0, 1201)
for per, col, lab in [(0.0005, BLUE, "gentle use (0.05% per cycle)"), (0.001, ORANGE, "hot or fast-charged (0.1%)")]:
    axes[0].plot(n, 100 * (1 - per) ** n, color=col, lw=2.5, label=lab)
axes[0].axhline(80, color=BLACK, ls="--"); axes[0].text(20, 81.5, "replace at 80%", fontsize=10)
axes[0].set_xlabel("full cycles"); axes[0].set_ylabel("capacity left (%)"); axes[0].grid(alpha=0.3); axes[0].legend(fontsize=9.5); axes[0].set_ylim(30, 102)
axes[0].set_title("capacity fades with use (Chapter 52)", fontsize=11)
T = np.array([-20, -10, 0, 10, 25, 40])
cap = np.array([55, 70, 82, 92, 100, 102]); res = np.array([4.0, 2.8, 1.9, 1.35, 1.0, 0.85])
axes[1].plot(T, cap, "o-", color=BLUE, lw=2.5, label="usable capacity (%)")
ax2 = axes[1].twinx(); ax2.plot(T, res, "s--", color=RED, lw=2.5, label="internal resistance (x room value)")
axes[1].set_xlabel("temperature (C)"); axes[1].set_ylabel("usable capacity (%)", color=BLUE); ax2.set_ylabel("resistance (x room value)", color=RED)
axes[1].grid(alpha=0.3); axes[1].set_title("cold: less capacity, more sag", fontsize=11)
save(fig, "fig06-ageing-cold.png")
print("saved 6 figures")
