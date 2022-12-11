import util
import numpy as np
import numpy.typing as npt
from functools import partial

s = np.array([util.split(line, int) for line in util.read_lines("inputs/day8.txt")])


def is_higher(value, row: npt.NDArray):
    if len(row) == 0:
        return True
    return np.all(row < value)


def view_distance(value, row: npt.NDArray):
    if len(row) == 0:
        return 0
    occluded = (row >= value).cumsum() > 0
    if not any(occluded):
        return len(occluded)
    return occluded.argmax() + 1


best_scenic_score = 0
for row in range(len(s)):
    for col in range(len(s[row, :])):
        left = np.flip(s[row, :col])
        right = s[row, col+1:]
        up = np.flip(s[:row, col])
        down = s[row+1:, col]
        score = partial(view_distance, s[row, col])
        scenic_score = score(left) * score(right) * score(up) * score(down)
        best_scenic_score = max(best_scenic_score, scenic_score)

print(best_scenic_score)
