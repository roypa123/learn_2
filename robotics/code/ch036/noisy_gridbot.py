# noisy_gridbot.py - what happens to the explorer when its sensors sometimes lie?
import random

from gridbot import GridBot, follow_right_wall, load_default_world

random.seed(7)


class NoisyBot(GridBot):
    """A GridBot whose wall sensor gives the wrong answer some of the time."""

    def __init__(self, world, error_chance):
        super().__init__(world)
        self.error_chance = error_chance

    def wall_at(self, side):
        truth = super().wall_at(side)
        if random.random() < self.error_chance:
            return not truth                  # the sensor lies
        return truth


world = load_default_world()
RUNS = 300

print("sensor error   reached goal   average bumps   average moves")
for error_chance in (0.0, 0.01, 0.05, 0.1, 0.2):
    wins = bumps = moves = 0
    for _ in range(RUNS):
        bot = NoisyBot(world, error_chance)
        wins += follow_right_wall(bot)        # True counts as 1 (Chapter 17)
        bumps += bot.bumps
        moves += bot.moves
    print(f"{error_chance:10.0%} {wins / RUNS:14.0%} {bumps / RUNS:15.1f} {moves / RUNS:15.1f}")
