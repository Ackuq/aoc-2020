from enum import Enum
from typing import Dict, List, Tuple


file = "input"

input = list(map(list, open("./{}.txt".format(file)).read().split("\n")))
input.reverse()


CYCLES = 6


class CubeState(Enum):
    ACTIVE = "#"
    INACTIVE = "."


Triple = Tuple[int, int, int]
Quadruple = Tuple[int, int, int, int]

TripleList = List[Triple]
QuadrupleList = List[Quadruple]


def parseInput() -> List[Tuple[int, int]]:
    initial_active: List[Tuple[int, int]] = []
    for y, row in enumerate(input):
        for x, cell in enumerate(row):
            if cell == CubeState.ACTIVE.value:
                initial_active.append((x, y))
    return initial_active


class State1:
    Cell = Triple
    active: TripleList = []

    def __init__(self, active: List[Triple]) -> None:
        self.active = active

    def count_neighbors(self) -> Dict[Triple, int]:
        active_neighbors: Dict[Triple, int] = {}
        for (x, y, z) in self.active:
            for neighbor_z in range(z - 1, z + 2):
                for neighbor_y in range(y - 1, y + 2):
                    for neighbor_x in range(x - 1, x + 2):
                        neighbor = (neighbor_x, neighbor_y, neighbor_z)
                        if neighbor != (x, y, z):
                            if neighbor in active_neighbors:
                                active_neighbors[neighbor] = (
                                    active_neighbors[neighbor] + 1
                                )
                            else:
                                active_neighbors[neighbor] = 1
        return active_neighbors

    def transition(self):
        active_neighbors = self.count_neighbors()

        new_active = []
        for active_neighbor, count in active_neighbors.items():
            if active_neighbor in self.active:
                if count in range(2, 4):
                    new_active.append(active_neighbor)
            else:
                if count == 3:
                    new_active.append(active_neighbor)

        self.active = new_active

    def run(self, cycles: int):
        cycle = 0
        while cycle < cycles:
            self.transition()
            cycle += 1


class State2(State1):
    Cell = Quadruple
    active: QuadrupleList = []

    def __init__(self, active: QuadrupleList) -> None:
        self.active = active

    def count_neighbors(self) -> Dict[Quadruple, int]:
        active_neighbors: Dict[Quadruple, int] = {}
        for (x, y, z, w) in self.active:
            for neighbor_w in range(w - 1, w + 2):
                for neighbor_z in range(z - 1, z + 2):
                    for neighbor_y in range(y - 1, y + 2):
                        for neighbor_x in range(x - 1, x + 2):
                            neighbor = (neighbor_x, neighbor_y, neighbor_z, neighbor_w)
                            if neighbor != (x, y, z, w):
                                if neighbor in active_neighbors:
                                    active_neighbors[neighbor] = (
                                        active_neighbors[neighbor] + 1
                                    )
                                else:
                                    active_neighbors[neighbor] = 1
        return active_neighbors


def part1():
    initial_active: TripleList = list(
        map(lambda cell: (cell[0], cell[1], 0), parseInput())
    )
    state = State1(initial_active)

    state.run(CYCLES)

    return len(state.active)


def part2():
    initial_active: QuadrupleList = list(
        map(lambda cell: (cell[0], cell[1], 0, 0), parseInput())
    )

    state = State2(initial_active)

    state.run(CYCLES)

    return len(state.active)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
