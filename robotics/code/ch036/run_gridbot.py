# run_gridbot.py - explore the maze, save a log, and draw a picture of the result
import csv

import matplotlib.pyplot as plt
import numpy as np

from gridbot import GridBot, draw, follow_right_wall, load_default_world, shortest_path

world = load_default_world()
print(draw(world))
print()

bot = GridBot(world)
reached = follow_right_wall(bot)
print(draw(bot=bot, world=world))
print("reached the goal:", reached)
print(bot)

best = shortest_path(world)
print("shortest path:", len(best) - 1, "moves")
print(draw(world, path=best))

with open("gridbot_log.csv", "w", newline="") as f:      # Chapter 27
    writer = csv.writer(f)
    writer.writerow(["step", "x", "y", "heading"])
    writer.writerows(bot.log)

visits = np.zeros((world.height, world.width))           # Chapter 34
for _, x, y, _ in bot.log:
    visits[y, x] += 1

fig, ax = plt.subplots(figsize=(8, 6))                   # Chapter 33
image = ax.imshow(np.ma.masked_equal(visits, 0), cmap="viridis")
walls = np.array([[1 if not world.is_free(x, y) else np.nan for x in range(world.width)] for y in range(world.height)])
ax.imshow(walls, cmap="gray_r", vmin=0, vmax=1.5)
xs = [row[1] for row in bot.log]
ys = [row[2] for row in bot.log]
ax.plot(xs, ys, color="white", linewidth=1)
fig.colorbar(image, label="log entries in this cell")
ax.set_title(f"GridBot: {bot.moves} moves to the goal (shortest possible: {len(best) - 1})")
fig.savefig("gridbot_result.png", dpi=150, bbox_inches="tight")
print("saved gridbot_log.csv and gridbot_result.png")
