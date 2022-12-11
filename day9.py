import util
import numpy as np
import numpy.typing as npt

positions = np.zeros((10, 2))


def get_delta(t: npt.NDArray, h: npt.NDArray) -> npt.NDArray:
    diff = h-t
    if any(abs(diff) > 1):
        return np.sign(h-t)
    return np.zeros((2,))


delta = {"U": np.array([0, 1]), "D": np.array([0, -1]), "L": np.array([-1, 0]), "R": np.array([1, 0])}
known_positions = set()
for line in util.read_lines("inputs/day9.txt"):
    direction, length = line.split()
    for _ in range(int(length)):
        positions[9] += delta[direction]
        for i in reversed(range(0, 9)):
            positions[i] += get_delta(positions[i], positions[i+1])

        known_positions.add(tuple(positions[0]))

print(len(known_positions))
