from typing import Dict, Tuple


file = "input.txt"


input = list(map(int, open("./{}".format(file)).read().split(",")))


MAX_ROUND = 30000000


def part1():
    round = 1
    prev: Dict[int, Tuple[int, int]] = {}

    for i in input:
        prev[i] = (-1, round)
        round += 1

    spoken = input.copy().pop()

    while round <= MAX_ROUND:
        if spoken in prev and prev[spoken][0] != -1:
            spoken = prev[spoken][1] - prev[spoken][0]
        elif spoken in prev:
            spoken = 0
        else:
            spoken = 0

        if spoken in prev:
            prev[spoken] = (prev[spoken][1], round)
        else:
            prev[spoken] = (-1, round)
        round += 1

    return spoken


if __name__ == "__main__":
    print("Part 1: ", part1())
