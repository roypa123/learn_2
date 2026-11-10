# first_plot.py - Rover's drive to the wall as a graph
import matplotlib.pyplot as plt

SETPOINT_M = 0.30
MAX_SPEED_MS = 0.25
DT_S = 0.5

times, distances = [0.0], [1.0]
distance_m = 1.0
for step in range(1, 13):
    speed_ms = min(MAX_SPEED_MS, distance_m - SETPOINT_M)     # gain 1, with the clamp
    distance_m -= speed_ms * DT_S
    times.append(step * DT_S)
    distances.append(distance_m)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(times, distances, "o-", label="distance")
ax.axhline(SETPOINT_M, color="black", linestyle="--", label="setpoint")
ax.set_xlabel("time (s)")
ax.set_ylabel("distance to wall (m)")
ax.set_title("Rover drives to the wall")
ax.grid(True)
ax.legend()
fig.savefig("first_plot.png", dpi=150)
print("saved first_plot.png")
print("final distance:", round(distances[-1], 3), "m")
