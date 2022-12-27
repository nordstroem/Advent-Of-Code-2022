import util
from functools import partial, lru_cache


grid = util.read_file("inputs/day24.txt").strip()
grid = util.to_numpy_grid(grid)
ROWS, COLS = grid.shape
GOAL = (ROWS-1, list(grid[-1, :]).index("."))
START = (0, 1)
walls = set()
current_blizzard = 0
blizzard_directions = {}
blizzards = set()


def heuristic(goal, state):
    return abs(state[0][0] - goal[0]) + abs(state[0][1] - goal[1])


def goal(goal, state):
    return state[0] == goal


@lru_cache(maxsize=None)
def get_new_blizzards(blizzards):
    new_blizzards = set()
    new_blizzard_pos = dict()
    for dir, r, c in blizzards:
        if dir == 0:
            p = (r, ((c-1-1) % (COLS-2))+1)
        elif dir == 1:
            p = (r, ((c+1-1) % (COLS-2))+1)
        elif dir == 2:
            p = (((r-1-1) % (ROWS-2))+1, c)
        else:
            p = (((r+1-1) % (ROWS-2))+1, c)
        new_blizzards.add((dir, *p))
        new_blizzard_pos[p] = True

    return frozenset(new_blizzards), new_blizzard_pos


@lru_cache(maxsize=None)
def in_walls(pos, walls):
    return pos in walls


def neighbors(walls, state):
    new_blizzards, new_blizzards_pos = get_new_blizzards(state[1])

    def valid(test_pos):
        return not in_walls(test_pos, walls) and test_pos not in new_blizzards_pos.keys()

    r, c = state[0]
    nbs = [(r, c), (r-1, c), (r+1, c), (r, c-1), (r, c+1)]
    new_blizzards = frozenset(new_blizzards)
    return [((n, new_blizzards), 1) for n in nbs if valid(n)]


walls.add((-1, 1))
for r in range(ROWS):
    for c in range(COLS):
        match grid[r, c]:
            case "#":
                walls.add((r, c))
            case "<" | ">" | "^" | "v" as dir:
                f = {"<": 0, ">": 1, "^": 2, "v": 3}
                blizzards.add((f[dir], r, c))

start = (START, frozenset(blizzards))
neighbors_func = partial(neighbors, frozenset(walls))
path = util.a_star(start, partial(goal, GOAL), partial(heuristic, GOAL), neighbors_func)
path2 = util.a_star(path[-1], partial(goal, START), partial(heuristic, START), neighbors_func)
path3 = util.a_star(path2[-1], partial(goal, GOAL), partial(heuristic, GOAL), neighbors_func)
print(len(path) + len(path2) + len(path3) - 3)
