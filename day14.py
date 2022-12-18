import util
from collections import defaultdict
from itertools import pairwise

grid = defaultdict(int)

lines = util.read_lines("inputs/day14.txt")

max_rock_y = 0
for line in lines:
    ints = util.extract_ints(line)
    coords = [(ints[i], ints[i+1]) for i in range(0, len(ints), 2)]
    for a, b in pairwise(coords):
        from_x, to_x = min(a[0], b[0]), max(a[0], b[0])
        from_y, to_y = min(a[1], b[1]), max(a[1], b[1])
        max_rock_y = max(max_rock_y, to_y)
        for x in range(from_x, to_x+1):
            for y in range(from_y, to_y+1):
                grid[(x, y)] = 1

ans = 0
sand_pos = (500, 0)
while True:
    if grid[(500, 0)] == 1:
        break

    if sand_pos[1] < max_rock_y + 1:
        test_pos = (sand_pos[0], sand_pos[1] + 1)
        if grid[test_pos] == 0:
            sand_pos = test_pos
            continue
        test_pos = (sand_pos[0] - 1, sand_pos[1] + 1)
        if grid[test_pos] == 0:
            sand_pos = test_pos
            continue
        test_pos = (sand_pos[0] + 1, sand_pos[1] + 1)
        if grid[test_pos] == 0:
            sand_pos = test_pos
            continue

    grid[sand_pos] = 1
    ans += 1
    sand_pos = (500, 0)

print(ans)
