import util

m = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}


def to_decimal(s):
    ans = 0
    for index, c in enumerate(reversed(s)):
        ans += m[c] * 5**index
    return ans


def to_snafu(n):
    snafu = ""
    while n:
        r = n % 5
        if r == 0 or r == 1 or r == 2:
            snafu = str(r) + snafu
            n = n // 5
        else:
            if r == 3:
                snafu = "=" + snafu
            else:
                snafu = "-" + snafu
            n = (n) // 5 + 1

    return snafu


target = sum(util.read_lines("inputs/day25.txt", to_decimal))
print(to_snafu(target))
