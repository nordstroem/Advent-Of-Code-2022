import util
import networkx as nx
from dataclasses import dataclass
import operator
from typing import Callable, Optional
import sympy as sp


@dataclass
class Node:
    op: Callable[..., int]
    left: Optional[str] = None
    right: Optional[str] = None


ops = {
    "+": operator.iadd,
    "-": operator.isub,
    "*": operator.imul,
    "/": operator.itruediv,
}

graph = nx.DiGraph()
expressions = {}
nodes = {}
x = sp.symbols("x")

for line in util.read_lines("inputs/day21.txt"):
    name, rest = line.split(":")
    rest = rest.strip()
    if rest.isdigit():
        if name == "humn":
            expressions[name] = x
        else:
            expressions[name] = int(rest)
        graph.add_node(name)
    else:
        left, op, right = rest.split()
        if name == "root":
            nodes[name] = Node(lambda l, r: sp.solve(l - r, x), left, right)
        else:
            nodes[name] = Node(ops[op], left, right)
        graph.add_edge(left, name)
        graph.add_edge(right, name)


for name in nx.topological_sort(graph):
    if name not in expressions:
        node = nodes[name]
        expressions[name] = node.op(expressions[node.left], expressions[node.right])

print(int(expressions["root"]))
