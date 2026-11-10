# gridbot.py - a small robot simulator: a world, a robot, and a way to explore
from collections import deque
from pathlib import Path

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
STEP = {NORTH: (0, -1), EAST: (1, 0), SOUTH: (0, 1), WEST: (-1, 0)}     # (dx, dy); y grows downward
ARROW = {NORTH: "^", EAST: ">", SOUTH: "v", WEST: "<"}


class World:
    """A grid of walls and floor, loaded from lines of text."""

    def __init__(self, lines):
        self.rows = [line.rstrip("\n") for line in lines if line.strip()]
        self.height = len(self.rows)
        self.width = max(len(row) for row in self.rows)
        self.start = self._find("S")
        self.goal = self._find("G")

    @classmethod
    def from_file(cls, path):
        """Make a World from a text file."""
        with open(path) as f:
            return cls(f.readlines())

    def _find(self, letter):
        for y, row in enumerate(self.rows):
            x = row.find(letter)
            if x != -1:
                return x, y
        raise ValueError(f"the map has no {letter}")

    def is_free(self, x, y):
        """Return True if the cell is inside the map and is not a wall."""
        if not (0 <= y < self.height and 0 <= x < len(self.rows[y])):
            return False
        return self.rows[y][x] != "#"


class GridBot:
    """A robot that lives on the grid. It can only do what its sensors allow."""

    BATTERY_START = 300

    def __init__(self, world, heading=EAST):
        self.world = world
        self.x, self.y = world.start
        self.heading = heading
        self.battery = self.BATTERY_START
        self.moves = 0
        self.bumps = 0
        self.visited = {(self.x, self.y)}
        self.log = [(0, self.x, self.y, self.heading)]

    def _record(self):
        self.battery -= 1
        self.log.append((len(self.log), self.x, self.y, self.heading))

    def left(self):
        self.heading = (self.heading - 1) % 4
        self._record()

    def right(self):
        self.heading = (self.heading + 1) % 4
        self._record()

    def _cell_towards(self, heading):
        dx, dy = STEP[heading]
        return self.x + dx, self.y + dy

    def forward(self):
        """Move one cell. Hitting a wall costs a bump and the robot stays put."""
        x, y = self._cell_towards(self.heading)
        if self.world.is_free(x, y):
            self.x, self.y = x, y
            self.moves += 1
            self.visited.add((x, y))
        else:
            self.bumps += 1
        self._record()

    def wall_at(self, side):
        """Sensor: is there a wall to the 'front', 'left' or 'right'?"""
        offset = {"front": 0, "right": 1, "left": -1}[side]
        return not self.world.is_free(*self._cell_towards((self.heading + offset) % 4))

    def at_goal(self):
        return (self.x, self.y) == self.world.goal

    def __str__(self):
        return (f"at ({self.x}, {self.y}) facing {ARROW[self.heading]}, moves {self.moves}, "
                f"bumps {self.bumps}, battery {self.battery}, cells {len(self.visited)}")


def follow_right_wall(bot, max_steps=1000):
    """Keep a hand on the right-hand wall until the goal. Return True on success."""
    steps = 0
    while not bot.at_goal() and steps < max_steps and bot.battery > 0:
        if not bot.wall_at("right"):
            bot.right()
            bot.forward()
        elif not bot.wall_at("front"):
            bot.forward()
        else:
            bot.left()
        steps += 1
    return bot.at_goal()


def shortest_path(world):
    """Breadth-first search: return the list of cells from start to goal, or None."""
    came_from = {world.start: None}
    queue = deque([world.start])
    while queue:
        cell = queue.popleft()
        if cell == world.goal:
            path = []
            while cell is not None:
                path.append(cell)
                cell = came_from[cell]
            return path[::-1]
        for dx, dy in STEP.values():
            neighbour = (cell[0] + dx, cell[1] + dy)
            if world.is_free(*neighbour) and neighbour not in came_from:
                came_from[neighbour] = cell
                queue.append(neighbour)
    return None


def draw(world, bot=None, path=None):
    """Return the map as text, with the visited cells and the robot marked."""
    grid = [list(row) for row in world.rows]
    if bot is not None:
        for x, y in bot.visited:
            if grid[y][x] == ".":
                grid[y][x] = "o"
    if path is not None:
        for x, y in path:
            if grid[y][x] in ".o":
                grid[y][x] = "*"
    if bot is not None:
        grid[bot.y][bot.x] = ARROW[bot.heading]
    return "\n".join("".join(row) for row in grid)


def load_default_world():
    return World.from_file(Path(__file__).parent / "worlds" / "maze.txt")
