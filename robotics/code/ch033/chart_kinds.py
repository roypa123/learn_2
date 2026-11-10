# chart_kinds.py - four useful kinds of chart in one figure
import random

import matplotlib.pyplot as plt

random.seed(1)

fig, axes = plt.subplots(2, 2, figsize=(9, 6))

axes[0, 0].plot([0, 1, 2, 3], [0, 1, 4, 9], "o-")
axes[0, 0].set_title("plot: a value that changes")

axes[0, 1].scatter([random.random() for _ in range(40)], [random.random() for _ in range(40)])
axes[0, 1].set_title("scatter: separate points")

axes[1, 0].bar(["motors", "brain", "sensors"], [3.0, 0.55, 0.23], color="tab:orange")
axes[1, 0].set_title("bar: comparing amounts (W)")

axes[1, 1].hist([random.gauss(0, 1) for _ in range(1000)], bins=25, color="tab:green")
axes[1, 1].set_title("hist: how values are spread")

fig.tight_layout()
fig.savefig("chart_kinds.png", dpi=150)
print("saved chart_kinds.png")
