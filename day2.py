from util import *
lines = read_lines("inputs/day2.txt", lambda x: (x[0], x[2]))

# R P S
scores = {"A": 1, "B": 2, "C": 3}

win = {"A": "B", "B": "C", "C": "A"}
loss = {b: a for a, b in win.items()}
draw = {"A": "A", "B": "B", "C": "C"}


def get_score(other, rule):
    match rule:
        case "X":
            return scores[loss[other]]
        case "Y":
            return scores[draw[other]] + 3
        case _:
            return scores[win[other]] + 6


total_score = 0
for a, rule in lines:
    total_score += get_score(a, rule)

print(total_score)
