# test_gridbot.py - prove that the simulator behaves as it should
from gridbot import EAST, NORTH, SOUTH, WEST, GridBot, World, follow_right_wall, shortest_path

TINY = ["#####",
        "#S.G#",
        "#####"]


def test_world_loads():
    world = World(TINY)
    assert (world.width, world.height) == (5, 3)
    assert world.start == (1, 1)
    assert world.goal == (3, 1)


def test_walls_and_edges():
    world = World(TINY)
    assert world.is_free(2, 1)
    assert not world.is_free(0, 0)
    assert not world.is_free(-1, 1)        # outside the map
    assert not world.is_free(99, 1)


def test_turning_wraps():
    bot = GridBot(World(TINY), heading=NORTH)
    bot.left()
    assert bot.heading == WEST
    bot.right()
    bot.right()
    assert bot.heading == EAST


def test_forward_and_bump():
    bot = GridBot(World(TINY), heading=EAST)
    bot.forward()
    assert (bot.x, bot.y, bot.moves, bot.bumps) == (2, 1, 1, 0)
    bot.heading = SOUTH
    bot.forward()
    assert (bot.x, bot.y, bot.moves, bot.bumps) == (2, 1, 1, 1)    # did not move


def test_sensors():
    bot = GridBot(World(TINY), heading=EAST)
    assert not bot.wall_at("front")
    assert bot.wall_at("left")
    assert bot.wall_at("right")


def test_battery_runs_down():
    bot = GridBot(World(TINY))
    start = bot.battery
    bot.left()
    bot.forward()
    assert bot.battery == start - 2


def test_reaches_goal():
    bot = GridBot(World(TINY))
    assert follow_right_wall(bot) is True


def test_shortest_path():
    assert shortest_path(World(TINY)) == [(1, 1), (2, 1), (3, 1)]


def test_no_route():
    blocked = ["#####", "#S#G#", "#####"]
    assert shortest_path(World(blocked)) is None


def test_missing_goal():
    try:
        World(["###", "#S#", "###"])
    except ValueError as error:
        assert "no G" in str(error)
    else:
        raise AssertionError("a map with no goal should be refused")


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("ok  ", test.__name__)
    print(len(tests), "tests passed")
