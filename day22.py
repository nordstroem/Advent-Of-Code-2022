import util
import numpy as np


class Dir:
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


rotate_R = {Dir.RIGHT: Dir.DOWN, Dir.DOWN: Dir.LEFT, Dir.LEFT: Dir.UP, Dir.UP: Dir.RIGHT}
rotate_L = {Dir.RIGHT: Dir.UP, Dir.UP: Dir.LEFT, Dir.LEFT: Dir.DOWN, Dir.DOWN: Dir.RIGHT}
opposite = {Dir.RIGHT: Dir.LEFT, Dir.UP: Dir.DOWN, Dir.LEFT: Dir.RIGHT, Dir.DOWN: Dir.UP}

EMPTY = ord(" ")
PATH = ord(".")
WALL = ord("#")

grid, path = util.read_file("inputs/day22.txt").split("\n\n")

grid = np.pad(util.to_numpy_grid(grid).view(int), (1, 1), mode="constant", constant_values=EMPTY)

row = 1
col = (grid == PATH).argmax(axis=1)[row]
facing = Dir.RIGHT

steps_list = list(map(int, path.replace("R", " ").replace("L", " ").split()))
directions = path.translate({d: ord(" ") for d in range(ord("0"), ord("9")+1)}).split()

instructions = steps_list + directions
instructions[::2] = steps_list
instructions[1::2] = directions


def get_front(row, col, facing):
    match facing:
        case Dir.RIGHT:
            return grid[row, col:]
        case Dir.LEFT:
            return np.flip(grid[row, :col+1])
        case Dir.DOWN:
            return grid[row:, col]
        case _:
            return np.flip(grid[:row+1, col])


def get_direction(facing):
    match facing:
        case Dir.RIGHT:
            return (0, 1)
        case Dir.LEFT:
            return (0, -1)
        case Dir.DOWN:
            return (1, 0)
        case _:
            return (-1, 0)


def move(pos, facing, steps):
    row, col = pos
    while steps > 0:
        front = get_front(row, col, facing)
        dr, dc = get_direction(facing)
        first_wall = np.sign(np.cumsum(front == WALL)).argmax()
        first_empty = np.sign(np.cumsum(front == EMPTY)).argmax()
        if (steps < first_wall or first_wall == 0) and steps < first_empty:  # Can walk
            col += dc * steps
            row += dr * steps
            steps = 0
        elif first_wall != 0 and first_wall <= steps and first_wall < first_empty:  # Wall
            col += dc * (first_wall - 1)
            row += dr * (first_wall - 1)
            steps = 0
        else:  # Need to wrap around
            other_front = get_front(row, col, opposite[facing])
            other_empty = np.sign(np.cumsum(other_front == EMPTY)).argmax()
            wrap_pos_col = col - dc*(other_empty - 1)
            wrap_pos_row = row - dr*(other_empty - 1)
            if grid[wrap_pos_row, wrap_pos_col] == PATH:
                steps -= first_empty
                col = wrap_pos_col
                row = wrap_pos_row
            else:
                col += dc*(first_empty - 1)
                row += dr*(first_empty - 1)
                steps = 0
    return (row, col)


# assert move((8, 8), Dir.DOWN, 5) == (8, 6)
# assert move((4, 9), Dir.LEFT, 1) == (4, 12)
# assert move((4, 9), Dir.LEFT, 2) == (4, 11)
# assert move((1, 11), Dir.LEFT, 1) == (1, 10)
# assert move((3, 10), Dir.RIGHT, 4) == (3, 12)
# assert move((4, 9), Dir.RIGHT, 4) == (4, 9)
# assert move((4, 9), Dir.RIGHT, 5) == (4, 10)
# assert move((4, 9), Dir.RIGHT, 8) == (4, 9)
# assert move((1, 9), Dir.RIGHT, 10) == (1, 11)
# assert move((1, 9), Dir.RIGHT, 1) == (1, 10)
# assert move((1, 9), Dir.RIGHT, 2) == (1, 11)


for instruction in instructions:
    match instruction, facing:
        case "R", _:
            facing = rotate_R[facing]
        case "L", _:
            facing = rotate_L[facing]
        case int(steps), _:
            row, col = move((row, col), facing, steps)

print(row*1000 + col*4 + facing)
