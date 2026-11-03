# plot_catch.py - the hand from Chapter 6, now drawn as a graph
import matplotlib.pyplot as plt

setpoint = 1.2        # the ball lands 1.2 m to the right
dt = 0.05             # one loop every 0.05 s

for gain in [1, 4, 30]:
    hand = 0.0
    times = []                            # an empty list for the times
    positions = []                        # an empty list for the hand positions
    for step in range(21):
        times.append(step * dt)           # remember this time ...
        positions.append(hand)            # ... and where the hand was
        error = setpoint - hand
        hand = hand + gain * error * dt
    print("gain", gain, "| hand at 1.0 s:", round(positions[20], 3), "m")
    plt.plot(times, positions, marker="o", label="gain " + str(gain))

plt.axhline(setpoint, color="black", linestyle="--", label="setpoint")
plt.xlabel("time (s)")
plt.ylabel("hand position (m)")
plt.title("Catching a ball with three different gains")
plt.legend()
plt.savefig("catch_plot.png")
plt.show()
