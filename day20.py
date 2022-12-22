import util
import numpy as np
values = np.array(util.read_lines("inputs/day20.txt", int), dtype=np.int64)
values = values * 811589153
N = len(values)
indices = list(range(N))


def move(index, steps, values):
    new_values = values.copy()
    if abs(steps) >= len(values):
        steps = np.sign(steps) * (abs(steps) % (len(values) - 1))
    new_index = (index + steps) % len(values)
    value = values[index]
    if new_index > index:
        new_values.insert(new_index + 1 if steps > 0 else new_index, value)
        new_values.pop(index)
    else:
        new_values.pop(index)
        new_values.insert(new_index + 1 if steps > 0 else new_index, value)

    return new_values


for _ in range(10):
    for i in range(N):
        index = indices.index(i)
        indices = move(index, values[i], indices)


values = list(values[indices])
start = values.index(0)
print(values[(start+1000) % len(values)] + values[(start+2000) % len(values)] + values[(start+3000) % len(values)])
