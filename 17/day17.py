from enum import Enum
from typing import Iterator, List, Literal, Tuple, Union
from copy import deepcopy


file = "input"

input = list(map(list, open("./{}.txt".format(file)).read().split("\n")))
input.reverse()


CYCLES = 6


class CubeState(Enum):
    ACTIVE = "#"
    INACTIVE = "."


Cell1 = Tuple[int, int, int]
Cell2 = Tuple[int, int, int, int]

# x,y,z
Active1 = List[Cell1]

# x,y,z,w
Active2 = List[Cell2]


class State1:
    active: Active1 = []

    def __init__(self, active: Active1) -> None:
        self.active = active

    def max_x(self):
        return max(self.active, key=lambda coord: coord[0])[0]

    def min_x(self):
        return min(self.active, key=lambda coord: coord[0])[0]

    def max_y(self):
        return max(self.active, key=lambda coord: coord[1])[1]

    def min_y(self):
        return min(self.active, key=lambda coord: coord[1])[1]

    def max_z(self):
        return max(self.active, key=lambda coord: coord[2])[2]

    def min_z(self):
        return min(self.active, key=lambda coord: coord[2])[2]

    def print_state(self, cycle):
        print("\nAfter {} cycles\n".format(cycle))
        for z in range(self.min_z(), self.max_z() + 1):
            print("z={}".format(z))
            for y in range(self.max_y(), self.min_y() - 1, -1):
                row = ""
                for x in range(self.min_x(), self.max_x() + 1):
                    if (x, y, z) in self.active:
                        row += CubeState.ACTIVE.value
                    else:
                        row += CubeState.INACTIVE.value
                print(row)
            print("\n")


class State2(State1):
    active: Active2 = []

    def __init__(self, active: Active2) -> None:
        self.active = active

    def max_w(self):
        return max(self.active, key=lambda coord: coord[3])[3]

    def min_w(self):
        return min(self.active, key=lambda coord: coord[3])[3]

    def print_state(self, cycle):
        print("\nAfter {} cycles\n".format(cycle))
        for w in range(self.min_w(), self.max_w() + 1):
            for z in range(self.min_z(), self.max_z() + 1):
                print("z={}, w={}".format(z, w))
                for y in range(self.max_y(), self.min_y() - 1, -1):
                    row = ""
                    for x in range(self.min_x(), self.max_x() + 1):
                        if (x, y, z, w) in self.active:
                            row += CubeState.ACTIVE.value
                        else:
                            row += CubeState.INACTIVE.value
                    print(row)
                print("\n")


def part1():
    def parseInput() -> State1:
        initial_active: Active1 = []
        for y, row in enumerate(input):
            for x, cell in enumerate(row):
                if cell == CubeState.ACTIVE.value:
                    initial_active.append((x, y, 0))
        return State1(initial_active)

    def get_active_neighbors(coords: Cell1, state: State1) -> Active1:
        (x, y, z) = coords

        x_low = max(state.min_x(), x - 1)
        x_high = min(state.max_x() + 1, x + 2)
        y_low = max(state.min_y(), y - 1)
        y_high = min(state.max_y() + 1, y + 2)
        z_low = max(state.min_z(), z - 1)
        z_high = min(state.max_z() + 1, z + 2)

        neighbors: Active1 = []

        for neighbor_z in range(z_low, z_high):
            for neighbor_y in range(y_low, y_high):
                for neighbor_x in range(x_low, x_high):
                    if neighbor_z != z or neighbor_y != y or neighbor_x != x:
                        neighbors.append((neighbor_x, neighbor_y, neighbor_z))

        intersection = []
        for neighbor in neighbors:
            if neighbor in state.active:
                intersection.append(neighbor)

        return intersection

    state = parseInput()

    cycle = 0

    # state.print_state(0)

    while cycle < CYCLES:
        new_state = deepcopy(state)

        for z in range(state.min_z() - 1, state.max_z() + 2):
            for y in range(state.min_y() - 1, state.max_y() + 2):
                for x in range(state.min_x() - 1, state.max_x() + 2):
                    my_cell = (x, y, z)
                    neighbors = get_active_neighbors(my_cell, state)
                    if my_cell in state.active and not len(neighbors) in range(2, 4):
                        new_state.active.remove(my_cell)
                    elif my_cell not in state.active and len(neighbors) == 3:
                        new_state.active.append(my_cell)
        state = new_state
        cycle += 1
        # state.print_state(cycle)

    return len(state.active)


def part2():
    def parseInput() -> State2:
        initial_active: Active2 = []
        for y, row in enumerate(input):
            for x, cell in enumerate(row):
                if cell == CubeState.ACTIVE.value:
                    initial_active.append((x, y, 0, 0))

        return State2(initial_active)

    def get_active_neighbors(coords: Cell2, state: State2) -> Active2:
        (x, y, z, w) = coords

        x_low = max(state.min_x(), x - 1)
        x_high = min(state.max_x() + 1, x + 2)

        y_low = max(state.min_y(), y - 1)
        y_high = min(state.max_y() + 1, y + 2)

        z_low = max(state.min_z(), z - 1)
        z_high = min(state.max_z() + 1, z + 2)

        w_low = max(state.min_w(), w - 1)
        w_high = min(state.max_w() + 1, w + 2)

        neighbors: Active2 = []
        for neighbor_w in range(w_low, w_high):
            for neighbor_z in range(z_low, z_high):
                for neighbor_y in range(y_low, y_high):
                    for neighbor_x in range(x_low, x_high):
                        if (
                            neighbor_w != w
                            or neighbor_z != z
                            or neighbor_y != y
                            or neighbor_x != x
                        ):
                            neighbors.append(
                                (neighbor_x, neighbor_y, neighbor_z, neighbor_w)
                            )

        intersection = []
        for neighbor in neighbors:
            if neighbor in state.active:
                intersection.append(neighbor)

        return intersection

    state = parseInput()

    cycle = 0

    # state.print_state(0)

    while cycle < CYCLES:
        new_state = deepcopy(state)
        for w in range(state.min_w() - 1, state.max_w() + 2):
            for z in range(state.min_z() - 1, state.max_z() + 2):
                for y in range(state.min_y() - 1, state.max_y() + 2):
                    for x in range(state.min_x() - 1, state.max_x() + 2):
                        my_cell = (x, y, z, w)
                        active_neighbors = get_active_neighbors(my_cell, state)
                        if my_cell in state.active and not len(
                            active_neighbors
                        ) in range(2, 4):
                            new_state.active.remove(my_cell)
                        elif my_cell not in state.active and len(active_neighbors) == 3:
                            new_state.active.append(my_cell)
        state = new_state
        cycle += 1
        print(cycle)
        # state.print_state(cycle)

    state.print_state(cycle)

    return len(state.active)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
