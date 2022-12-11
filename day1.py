from util import *

lines = read_file("inputs/day1.txt").strip().split("\n\n")


def merge(line):
    return sum(map(int, line.split("\n")))


#print(max(map(merge, lines)))

all = list(map(merge, lines))
all.sort()

print(sum(all[-3:]))
