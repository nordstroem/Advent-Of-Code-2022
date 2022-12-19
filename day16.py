import util
from dataclasses import dataclass
from typing import List, Dict
from itertools import product


@dataclass(frozen=True, slots=True)
class Node:
    flow_rate: int
    nodes: List["str"]


def parse(line: str):
    line = line[1:].replace(";", "").replace(",", "").replace("=", "")
    translation = {l: None for l in range(ord("a"), ord("z") + 1)}
    line = line.translate(translation)
    parts = line.split()
    return parts


lines = util.read_lines("inputs/day16.txt", parse)

graph: Dict[str, Node] = {}

for name, flow_rate, *nodes in lines:
    graph[name] = Node(int(flow_rate), nodes)

cache = {}


MINUTES = 26


def dp(names: frozenset[str], minute: int, nodes_opened: frozenset[str]):
    key = (names, minute, nodes_opened)

    if key in cache:
        return cache[key]

    num_open = len(nodes_opened)
    if num_open < 2 and minute > 6:
        return 0
    if num_open < 3 and minute > 10:
        return 0
    if num_open < 5 and minute > 12:
        return 0
    if num_open < 7 and minute > 16:
        return 0
    if num_open < 8 and minute > 20:
        return 0
    if num_open < 11 and minute > 23:
        return 0

    if minute > MINUTES:
        return 0

    paths = []

    if len(names) == 1:
        first, second = tuple(names)[0], tuple(names)[0]
    else:
        first, second = tuple(names)

    for first_target, second_target in product(graph[first].nodes + [first], graph[second].nodes + [second]):
        released = 0
        new_nodes_opened = nodes_opened
        if first_target == first:
            if first in new_nodes_opened or graph[first].flow_rate == 0:  # Not a valid path
                continue
            released += graph[first].flow_rate * (MINUTES - minute)
            new_nodes_opened = new_nodes_opened.union({first})
        if second_target == second:
            if second in new_nodes_opened or graph[second].flow_rate == 0:  # Not a valid path
                continue
            released += graph[second].flow_rate * (MINUTES - minute)
            new_nodes_opened = new_nodes_opened.union({second})

        paths.append(released + dp(frozenset({first_target, second_target}), minute + 1, new_nodes_opened))

    res = max(paths)
    cache[key] = res
    return res


res = dp(frozenset({"AA", "AA"}), 1, frozenset())

print(res)
