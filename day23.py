import util
from collections import defaultdict

np_grid = util.read_file("inputs/day23.txt").strip()
np_grid = util.to_numpy_grid(np_grid)


def get_targets(elves, test_counter):
    all_targets = defaultdict(list)
    for elf in elves:
        N = (elf[0] - 1, elf[1])
        S = (elf[0] + 1, elf[1])
        W = (elf[0], elf[1]-1)
        E = (elf[0], elf[1]+1)
        NE = (elf[0] - 1, elf[1] + 1)
        NW = (elf[0] - 1, elf[1] - 1)
        SE = (elf[0] + 1, elf[1] + 1)
        SW = (elf[0] + 1, elf[1] - 1)

        def empty(p): return p not in elves

        if empty(N) and empty(S) and empty(W) and empty(E) and empty(NE) and empty(NW) and empty(SE) and empty(SW):
            continue

        def test_north(): return empty(N) and empty(NE) and empty(NW)
        def test_south(): return empty(S) and empty(SE) and empty(SW)
        def test_west(): return empty(W) and empty(NW) and empty(SW)
        def test_east(): return empty(E) and empty(NE) and empty(SE)
        tests = [(test_north, N), (test_south, S), (test_west, W), (test_east, E)]
        for i in range(4):
            test, direction = tests[(i+test_counter) % 4]
            if test():
                all_targets[direction].append(elf)
                break

    targets = {elves[0]: target for target, elves in all_targets.items() if len(elves) == 1}
    return targets


def move(elves, test_counter):
    targets = get_targets(elves, test_counter)
    new_elves = set()
    for elf in elves:
        if elf in targets:
            new_elves.add(targets[elf])
        else:
            new_elves.add(elf)
    return new_elves


def count_empty(elves):
    min_x = min(elves, key=lambda e: e[0])[0]
    max_x = max(elves, key=lambda e: e[0])[0]
    min_y = min(elves, key=lambda e: e[1])[1]
    max_y = max(elves, key=lambda e: e[1])[1]
    return (max_x - min_x+1) * (max_y - min_y+1) - len(elves)


elves = set()
rows, cols = np_grid.shape
for row in range(rows):
    for col in range(cols):
        if np_grid[row, col] == "#":
            elves.add((row, col))


i = 0
while True:
    new_elves = move(elves, i)
    if new_elves == elves:
        print(i+1)
        break
    elves = new_elves
    i += 1
