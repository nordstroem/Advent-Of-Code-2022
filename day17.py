import util
import numpy as np

blocked = set()
for x in range(7):
    blocked.add((x, 0))


def is_blocked(pos):
    if pos[0] < 0 or pos[0] >= 7 or tuple(pos) in blocked:
        return True
    return False


rocks = [
    np.array([(0, 0), (1, 0), (2, 0), (3, 0)]),
    np.array([(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]),
    np.array([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    np.array([(0, 0), (0, 1), (0, 2), (0, 3)]),
    np.array([(0, 0), (1, 0), (0, 1), (1, 1)])
]


directions = util.read_file("inputs/day17.txt").strip()
dir_counter = 0
height_added = np.zeros((1967,))

for i in range(1967):
    rock = rocks[i % 5]
    pos_y = max(blocked, key=lambda p: p[1])[1] + 4
    pos = np.array((2, pos_y))
    while True:
        dir = directions[dir_counter]
        dx = np.array((-1, 0)) if dir == "<" else np.array((1, 0))
        dy = np.array((0, -1))
        if not any(is_blocked(part + dx) for part in rock + pos):
            pos += dx
        dir_counter = (dir_counter + 1) % len(directions)
        if not any(is_blocked(part + dy) for part in rock + pos):
            pos += dy
        else:
            for part in (rock + pos):
                blocked.add(tuple(part))
            new_pos_y = max(blocked, key=lambda p: p[1])[1] + 4
            height_added[i] = new_pos_y - pos_y
            break


period = 1745
periodic_start = 1966 - period
num_wanted = 1000000000000 - periodic_start
k = (num_wanted // period)
m = (num_wanted % period)

res = np.sum(height_added[0:periodic_start]) + np.sum(height_added[periodic_start:periodic_start+period]) * k + np.sum(height_added[periodic_start:periodic_start+m])

print(res)
