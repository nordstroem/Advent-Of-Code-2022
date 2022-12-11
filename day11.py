from dataclasses import dataclass
from typing import List, Callable


@dataclass
class Monkey:
    operation: Callable[[int], int]
    test: Callable[[int], int]
    items: List[int]
    items_inspected: int = 0


monkeys = [
    Monkey(lambda x: x * 3, lambda x: 1 if x % 2 == 0 else 4, [66, 59, 64, 51]),
    Monkey(lambda x: x * 19, lambda x: 3 if x % 7 == 0 else 5, [67, 61]),
    Monkey(lambda x: x + 2, lambda x: 4 if x % 11 == 0 else 0, [86, 93, 80, 70, 71, 81, 56]),
    Monkey(lambda x: x * x, lambda x: 7 if x % 19 == 0 else 6, [94]),
    Monkey(lambda x: x + 8, lambda x: 5 if x % 3 == 0 else 1, [71, 92, 64]),
    Monkey(lambda x: x + 6, lambda x: 3 if x % 5 == 0 else 6, [58, 81, 92, 75, 56]),
    Monkey(lambda x: x + 7, lambda x: 7 if x % 17 == 0 else 2, [82, 98, 77, 94, 86, 81]),
    Monkey(lambda x: x + 4, lambda x: 2 if x % 13 == 0 else 0, [54, 95, 70, 93, 88, 93, 63, 50]),

]

for i in range(10000):
    for monkey in monkeys:
        while monkey.items:
            item = monkey.items.pop(0)
            new_item = monkey.operation(item)
            new_item = new_item % (2*7*11*19*3*5*17*13)
            monkey.items_inspected += 1
            to_monkey = monkey.test(new_item)
            monkeys[to_monkey].items.append(new_item)

monkeys.sort(key=lambda m: m.items_inspected, reverse=True)
print(monkeys[0].items_inspected * monkeys[1].items_inspected)
