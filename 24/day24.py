from enum import Enum
import re
from typing import Dict, List, Tuple

file_name = "input"

file = open("./{}.txt".format(file_name)).read()

REGEX = r"(ne|se|nw|sw|w|e)"


class Direction(Enum):
    NORTH_EAST = "ne"
    SOUTH_EAST = "se"
    NORTH_WEST = "nw"
    SOUTH_WEST = "sw"
    WEST = "w"
    EAST = "e"


Coordinate = Tuple[int, int]


def map_input(row: str) -> List[Direction]:
    matches: List[Direction] = re.findall(REGEX, row)
    return list(matches)


puzzle_input = list(map(map_input, file.split("\n")))


class ReferenceTile:
    flipped: List[Coordinate]

    def __init__(self) -> None:
        self.flipped = []

    def flip(self, moves: List[Direction]):
        x = 0
        y = 0
        for move in moves:
            if move == Direction.NORTH_EAST.value:
                x += 1
                y += 1
            elif move == Direction.SOUTH_EAST.value:
                x += 1
                y -= 1
            elif move == Direction.NORTH_WEST.value:
                x -= 1
                y += 1
            elif move == Direction.SOUTH_WEST.value:
                x -= 1
                y -= 1
            elif move == Direction.WEST.value:
                x -= 2
            elif move == Direction.EAST.value:
                x += 2

        coordinate = (x, y)
        if coordinate in self.flipped:
            self.flipped.remove(coordinate)
        else:
            self.flipped.append(coordinate)

    def pass_day(self):
        new_flipped = []
        neighbor_occurrence: Dict[Coordinate, int] = {}
        for black in self.flipped:
            x, y = black
            neighbors = [
                (x - 2, y),
                (x + 2, y),
                (x + 1, y + 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x - 1, y - 1),
            ]
            for neighbor in neighbors:
                if neighbor in neighbor_occurrence:
                    neighbor_occurrence[neighbor] += 1
                else:
                    neighbor_occurrence[neighbor] = 1
        for neighbor, value in neighbor_occurrence.items():
            if neighbor in self.flipped:
                if value <= 2:
                    new_flipped.append(neighbor)
            else:
                if value == 2:
                    new_flipped.append(neighbor)
        self.flipped = new_flipped


def part1(input: List[List[Direction]]) -> ReferenceTile:
    reference_tile = ReferenceTile()

    for tile in input:
        reference_tile.flip(tile)

    return reference_tile


def part2(input: List[List[Direction]]):
    reference_tile = part1(input)
    for _ in range(100):
        reference_tile.pass_day()

    return len(reference_tile.flipped)


if __name__ == "__main__":
    print("Part 1:", len(part1(puzzle_input.copy()).flipped))
    print("Part 2:", part2(puzzle_input.copy()))
