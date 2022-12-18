import util
from itertools import zip_longest
from functools import cmp_to_key

lines = util.read_file("inputs/day12.txt").strip().replace("\n\n", "\n").split("\n")
lines = list(map(lambda x: eval(x), lines))


def right_order(left, right):
    match left, right:
        case int(left), int(right) if left == right:
            return None
        case int(left), int(right):
            return right > left
        case list(left), int(right):
            return right_order(left, [right])
        case int(left), list(right):
            return right_order([left], right)
        case None, None:
            return None
        case None, _:
            return True
        case _, None:
            return False
        case list(left), list(right):
            for l, r in zip_longest(left, right):
                is_right_order = right_order(l, r)
                if is_right_order is None:
                    continue
                return is_right_order
        case _:
            assert False


lines.append([[2]])
lines.append([[6]])


def key_function(left, right):
    if right_order(left, right):
        return -1
    return 1


lines.sort(key=cmp_to_key(key_function))

a = lines.index([[2]]) + 1
b = lines.index([[6]]) + 1
print(a * b)
