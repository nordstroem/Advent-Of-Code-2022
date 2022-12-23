import math
from functools import reduce
import re
from typing import Callable, Any
import numpy as np
import numpy.typing as npt


def read_lines(path, fun: Callable[[str], Any] = lambda x: x):
    with open(path, 'r') as inp:
        lines = inp.readlines()
        return [fun(l.strip()) for l in lines]


def read_file(path):
    with open(path, 'r') as inp:
        return inp.read()


def count_if(container, predicate):
    count = 0
    for element in container:
        if predicate(element):
            count = count + 1
    return count


def split(line, fun=lambda x: x):
    return [fun(char) for char in line]


def lcm(*args):
    return reduce(lambda a, b: a * b // math.gcd(a, b), args)


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def extract_ints(string):
    return list(map(int, re.findall(r"-?\d+", string)))


def to_numpy_grid(blob) -> npt.NDArray:
    lines = blob.split("\n")
    max_cols = len(max(lines, key=lambda l: len(l)))
    rows = list(map(lambda l: split(l.ljust(max_cols)), lines))
    grid = np.array(rows)
    return grid
