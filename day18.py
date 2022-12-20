import util
import sys

cubes = list()

for line in util.read_lines("inputs/day18.txt"):
    pos = util.extract_ints(line)
    cubes.append(tuple(pos))

min_x = cubes[0][0]
max_x = cubes[0][0]
min_y = cubes[0][1]
max_y = cubes[0][1]
min_z = cubes[0][2]
max_z = cubes[0][2]


for cube in cubes[1:]:
    min_x = min(min_x, cube[0])
    max_x = max(max_x, cube[0])
    min_y = min(min_y, cube[1])
    max_y = max(max_y, cube[1])
    min_z = min(min_z, cube[2])
    max_z = max(max_z, cube[2])


def get_sides(cube):
    up = (cube[0], cube[1] + 1, cube[2])
    down = (cube[0], cube[1] - 1, cube[2])
    left = (cube[0] - 1, cube[1], cube[2])
    right = (cube[0] + 1, cube[1], cube[2])
    front = (cube[0], cube[1], cube[2] + 1)
    back = (cube[0], cube[1], cube[2] - 1)
    return [up, down, left, right, front, back]


cache = set()


def is_exterior(cube, visited):
    visited.add(cube)

    if cube[0] < min_x or cube[0] > max_x or cube[1] < min_y or cube[1] > max_y or cube[2] < min_z or cube[2] > max_z:
        return True

    for side in get_sides(cube):
        if side not in visited and side not in cubes:
            if is_exterior(side, visited):
                return True

    return False


sys.setrecursionlimit(10000)
area = 0
for cube in cubes:
    for side in get_sides(cube):
        if side in cache or (side not in cubes and is_exterior(side, set())):
            cache.add(side)
            area += 1


print(area)
