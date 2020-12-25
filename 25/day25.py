puzzle_input = open("./input.txt").read()
example = open("./example.txt").read()

input = puzzle_input

public_keys = list(map(int, input.split("\n")))


def get_loop_size(subject_number: int, goal: int) -> int:
    value = 1
    i = 1
    while True:
        value *= subject_number
        value = value % 20201227
        if value == goal:
            return i
        i += 1


def transform(subject_number: int, loop_size: int):
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value = value % 20201227
    return value


def part1(keys):
    [card_key, door_key] = keys
    card_loop_size = get_loop_size(7, card_key)
    return transform(door_key, card_loop_size)


if __name__ == "__main__":
    print("Part 1:", part1(public_keys.copy()))
