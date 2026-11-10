# random_cleaner.py - a robot that wanders at random: how much floor does it clean?
import random

random.seed(4)
WIDTH, HEIGHT = 20, 20
MOVES = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}


def clean(steps):
    """Wander for some steps. Return the fraction of the floor visited."""
    x, y = WIDTH // 2, HEIGHT // 2
    visited = {(x, y)}                # a set: Chapter 22
    for _ in range(steps):
        dx, dy = MOVES[random.choice("NSEW")]
        if 0 <= x + dx < WIDTH and 0 <= y + dy < HEIGHT:     # stay inside the room
            x, y = x + dx, y + dy
        visited.add((x, y))
    return len(visited) / (WIDTH * HEIGHT)


for steps in (100, 400, 1600, 6400):
    runs = [clean(steps) for _ in range(30)]
    print(f"{steps:5d} steps: {sum(runs) / len(runs):.0%} cleaned on average")
