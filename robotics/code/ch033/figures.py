# Figures for Chapter 33 — Plotting data with matplotlib.
# Run:  python figures.py      (runs the chapter's programs, and draws the labelled figure)
import os
import subprocess
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch033")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})

for name in ("first_plot", "plot_drive_log", "sensor_calibration", "chart_kinds"):
    subprocess.run([sys.executable, os.path.join(HERE, name + ".py")], cwd=OUT, check=True,
                   env=dict(os.environ, MPLBACKEND="Agg"), stdout=subprocess.DEVNULL)

# ---------- Figure 1: the parts of a figure ----------
fig, ax = plt.subplots(figsize=(10, 6))
t = [0, 1, 2, 3, 4, 5]
ax.plot(t, [1.0, 0.75, 0.5, 0.35, 0.31, 0.30], "o-", color="#0072B2", label="distance")
ax.axhline(0.30, color="black", ls="--", label="setpoint")
ax.set_xlabel("time (s)"); ax.set_ylabel("distance to wall (m)"); ax.set_title("Rover drives to the wall"); ax.grid(True); ax.legend()
fig.subplots_adjust(left=0.24, right=0.72, top=0.82, bottom=0.2)
kw = dict(xycoords="figure fraction", textcoords="figure fraction", fontsize=12, color="#D55E00", weight="bold",
          arrowprops=dict(arrowstyle="-|>", color="#D55E00", lw=1.8))
ax.annotate("ax.set_title(...)", xy=(0.62, 0.855), xytext=(0.74, 0.93), **kw)
ax.annotate("ax.legend()\nneeds label= in plot", xy=(0.70, 0.74), xytext=(0.75, 0.68), **kw)
ax.annotate("ax.plot(x, y)\none data line", xy=(0.36, 0.56), xytext=(0.75, 0.48), **kw)
ax.annotate("ax.grid(True)", xy=(0.60, 0.4), xytext=(0.75, 0.32), **kw)
ax.annotate("ax.set_ylabel(...)\nname AND unit", xy=(0.17, 0.5), xytext=(0.0, 0.72), **kw)
ax.annotate("ax.set_xlabel(...)", xy=(0.525, 0.135), xytext=(0.65, 0.06), **kw)
ax.text(-0.46, 1.17, "fig: the whole picture", transform=ax.transAxes, fontsize=12.5, weight="bold", color="#009E73")
ax.text(0.12, 0.9, "ax: one set of axes", transform=ax.transAxes, fontsize=12.5, weight="bold", color="#009E73")
fig.savefig(os.path.join(OUT, "fig01-parts-of-a-figure.png"), dpi=150)
plt.close(fig)
print("figures saved in", os.path.abspath(OUT))
