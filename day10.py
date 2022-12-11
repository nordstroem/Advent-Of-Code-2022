import util

cycle = 1
x = 1
for line in util.read_lines("inputs/day10.txt"):
    pixel = (cycle - 1) % 40
    match line.split():
        case "noop", :
            pixel = (cycle - 1) % 40
            if pixel == 0:
                print()
            if abs(x - pixel) < 2:
                print("#", end="")
            else:
                print(" ", end="")
            cycle += 1
        case "addx", value:
            for _ in range(2):
                pixel = (cycle - 1) % 40
                if pixel == 0:
                    print()
                if abs(x - pixel) < 2:
                    print("#", end="")
                else:
                    print(" ", end="")
                cycle += 1
            x += int(value)
