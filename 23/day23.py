from typing import Dict, List, Tuple, Union

my_input = 476138259
example = 389125467

puzzle_input = list(map(int, [i for i in str(my_input)]))


class Cup:
    key: int
    next: Union[None, "Cup"]

    def __init__(self, key: int) -> None:
        self.key = key

    def set_next(self, next: Union[None, "Cup"]):
        self.next = next

    def get_destination(
        self, picked_up: List[int], cup_map: Dict[int, "Cup"], largest=9
    ):
        i = self.key
        while True:
            i = i - 1 if i > 1 else largest
            if i not in picked_up:
                return cup_map[i]

    def pick_up(self) -> Tuple["Cup", "Cup", "Cup"]:
        start = self.next
        mid = start.next
        end = mid.next
        next_ = end.next
        assert start is not None
        assert mid is not None
        assert end is not None
        assert next_ is not None
        end.next = None

        return (start, end, next_)

    def multiply(self, length: int, acc: int):
        if length == acc:
            return self.key
        else:
            return self.key * self.next.multiply(length, acc + 1)


def parse_input(unparsed: List[int]) -> Tuple[Cup, Dict[int, Cup]]:
    result: Dict[int, Cup] = {}
    prev: Union[Cup, None] = None
    for key in unparsed:
        cup = Cup(key)
        result[key] = cup
        if prev is not None:
            prev.set_next(cup)

        prev = cup

    first = result[unparsed[0]]

    prev.set_next(first)

    return first, result


def to_string(start: Cup, length=None) -> str:
    end = start.key
    result = ""
    current = start.next
    i = 0
    while current.key != end and (length is None or i < length):
        result += str(current.key)
        current = current.next
        i += 1
    return result


def play_game(first, cup_map: Dict[int, Cup], rounds):
    current = first
    round = 1
    while round <= rounds:
        pick_up_s, pick_up_e, next_ = current.pick_up()
        current.set_next(next_)
        destination = current.get_destination(
            [pick_up_s.key, pick_up_s.next.key, pick_up_s.next.next.key],
            cup_map,
        )
        pick_up_e.set_next(destination.next)
        destination.set_next(pick_up_s)
        current = current.next

        round += 1

    return cup_map


def part1(input: List[int]):
    first, cup_map = parse_input(input)

    cup_map = play_game(first, cup_map, 100)

    return to_string(cup_map[1])


CUPS_2 = 1000000


def part2(input: List[int]):
    key_max = max(input)
    for i in range(key_max + 1, CUPS_2 + 1):
        input.append(i)

    first, cup_map = parse_input(input)

    cup_map = play_game(first, cup_map, 10000000)

    return cup_map[1].next.multiply(2, 1)


if __name__ == "__main__":
    print("Part 1:", part1(puzzle_input))
    print("Part 2:", part2(puzzle_input))
