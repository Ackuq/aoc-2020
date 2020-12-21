import re
from functools import reduce
from math import sqrt
from typing import Dict, List, Literal, Tuple, Union
from copy import deepcopy

input_file = "input"
input = open("./{}.txt".format(input_file)).read()

SYMBOLS = {"ACTIVE": "#", "INACTIVE": "."}


Coordinate = Tuple[int, int]
Active = List[Coordinate]
Content = List[List[str]]

AdjacentTiles = Dict[str, Union[int, None]]


class Tile:
    id: int
    content: Content
    adjacent_tiles: List[int]
    in_image = False

    rotated = 0

    def __init__(self, id: int, content: Content) -> None:
        self.id = id
        self.content = content
        self.adjacent_tiles = []

    def is_corner(self) -> bool:
        if len(self.adjacent_tiles) == 2:
            return True
        return False

    def get_named_sides(self) -> Dict[str, List[str]]:
        return {
            "up": list(self.content[0]),
            "right": list(map(lambda row: row[-1], self.content)),
            "down": list(self.content[-1]),
            "left": list(map(lambda row: row[0], self.content)),
        }

    def get_sides(self) -> List[List[str]]:
        sides = []
        sides.append(list(self.content[0]))
        sides.append(list(self.content[-1]))
        sides.append(list(map(lambda row: row[0], self.content)))
        sides.append(list(map(lambda row: row[-1], self.content)))
        return sides

    def print_tile(self):
        print("\n{}".format(self.id))
        for row in self.content:
            print("".join(row))

    def flip(self):
        self.content = list(reversed(self.content))

    def rotate(self):
        self.content = [list(a) for a in zip(*self.content[::-1])]
        self.rotated = (self.rotated + 90) % 360


Tiles = Dict[int, Tile]


def reduce_input(prev: Tiles, current: str):
    rows = current.split("\n")
    id = int(re.match(r"^Tile (\d+):$", rows.pop(0)).group(1))

    prev[id] = Tile(id, list(map(list, rows)))

    return prev


tiles_input = reduce(reduce_input, input.split("\n\n"), {})


def is_adjacent(tile1: Tile, tile2: Tile) -> bool:
    for side1 in tile1.get_sides():
        reversed1 = list(reversed(side1))
        for side2 in tile2.get_sides():
            if side1 == side2 or reversed1 == side2:
                return True

    return False


def is_adjacent_no_rotate(tile1: Tile, tile2: Tile) -> bool:
    sides1 = tile1.get_named_sides()
    sides2 = tile2.get_named_sides()

    if (
        sides1["up"] == sides2["down"]
        or sides1["left"] == sides2["right"]
        or sides1["down"] == sides2["up"]
        or sides1["right"] == sides2["left"]
    ):
        return True

    return False


def find_adjacent(tiles: Tiles):
    for tile in tiles.values():
        for possible_neighbor in tiles.values():
            if (
                tile.id != possible_neighbor.id
                and tile.id not in possible_neighbor.adjacent_tiles
            ):
                if is_adjacent(tile, possible_neighbor):
                    tile.adjacent_tiles.append(possible_neighbor.id)
                    possible_neighbor.adjacent_tiles.append(tile.id)

    return tiles


def find_corners(tiles: Tiles) -> Tiles:
    corners = {}
    for tile in tiles.values():
        if tile.is_corner():
            corners[tile.id] = tile
    return corners


def remove_borders(tiles: Tiles):
    for tile in tiles.values():
        tile.content.pop()
        tile.content.pop(0)
        for i in range(len(tile.content)):
            tile.content[i].pop()
            tile.content[i].pop(0)
    return tiles


def part1():
    tiles = deepcopy(tiles_input)
    tiles = find_adjacent(tiles)
    corners = find_corners(tiles)
    return reduce(lambda a, b: a * b, corners, 1)


def is_right_of(tile1: Tile, tile2: Tile):
    right = tile1.get_named_sides()["right"]
    left = tile2.get_named_sides()["left"]
    if right == left:
        return True
    return False


def is_below(tile1: Tile, tile2: Tile):
    up = tile1.get_named_sides()["up"]
    down = tile2.get_named_sides()["down"]
    if up == down:
        return True
    return False


def valid_placement(tile1, tile2, column: int, acc: List[List[Tile]]):
    if is_right_of(tile1, tile2) and (
        len(acc) == 0 or is_below(tile2, acc[-1][column])
    ):
        return True
    return False


def place_tile(tile: Tile, tiles: Tiles, column: int, acc: List[List[Tile]]):
    adjacent_tiles = [
        tiles[adjacent]
        for adjacent in tile.adjacent_tiles
        if not tiles[adjacent].in_image
    ]

    for adjacent in adjacent_tiles:
        for i in range(8):
            if valid_placement(tile, adjacent, column, acc):
                adjacent.in_image = True
                return adjacent
            if i == 3:
                adjacent.flip()
            else:
                adjacent.rotate()


def place_below(tile1: Tile, tile2: Tile, acc: List[List[Tile]]):
    if is_below(tile2, tile1):
        tile2.in_image = True
        return
    for i in range(0, 8):
        if i == 4:
            tile2.flip()
        else:
            tile2.rotate()
        if is_below(tile2, tile1):
            tile2.in_image = True
            return
    for t in acc[-1]:
        t.flip()

    place_below(tile1, tile2, acc)


def count_water(grid: List[List[str]]):
    count = 0
    for row in grid:
        count += sum(map(lambda x: x == "#", row))
    return count


def part2():
    tiles = deepcopy(tiles_input)
    size = int(sqrt(len(tiles)))
    tiles = find_adjacent(tiles)
    corners = find_corners(tiles)

    top_left = next(iter(corners.values()))
    image: List[List[Tile]] = []
    for _ in range(size):
        row = []
        if len(image) == 0:
            row.append(top_left)
            top_left.in_image = True
        else:
            tile = next(
                tiles[adjacent]
                for adjacent in image[-1][0].adjacent_tiles
                if not tiles[adjacent].in_image
            )
            place_below(image[-1][0], tile, image)
            row.append(tile)
        for i in range(size - 1):
            placed = place_tile(row[-1], tiles, i + 1, image)
            row.append(placed)
        image.append(row)

    tiles = remove_borders(tiles)

    image_content = []
    for i in range(len(image)):
        rows = len(image[i])
        j = 0
        while j < len(image[i][0].content):
            row = []
            for k in range(rows):
                row += image[i][k].content[j]
            j += 1
            image_content.append(row)

    image_tile = Tile(-1, image_content)
    monster = list(map(list, open("./monster.txt").read().split("\n")))

    monster_size = count_water(monster)
    image_water = count_water(image_tile.content)

    def find_monster_inner(offset_x, offset_y):
        for y in range(len(monster)):
            for x in range(len(monster[0])):
                if (
                    monster[y][x] == "#"
                    and image_tile.content[y + offset_y][x + offset_x] != "#"
                ):
                    return False
        return True

    count = 0
    for i in range(8):
        for offset_y in range(len(image_tile.content) - len(monster)):
            for offset_x in range(len(image_tile.content[0]) - len(monster[0])):
                if find_monster_inner(offset_x, offset_y):
                    count += 1
        if i == 4:
            image_tile.flip()
        else:
            image_tile.rotate()
    return image_water - (monster_size * count)


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
