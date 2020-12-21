import re
from typing import Dict, List, Set, Tuple


file_name = "input"
input = open("./{}.txt".format(file_name)).read()


class Food:
    ingredients: List[str]
    allergens: List[str]

    def __init__(self, ingredients: List[str], allergens: List[str]) -> None:
        self.ingredients = ingredients
        self.allergens = allergens


def map_food(row: str):
    match = re.search(r"\s\(contains\s(.+)\)", row)
    allergens = match.group(1).split(", ")
    ingredients = row.split(match.group(0))[0].split(" ")

    return Food(ingredients, allergens)


def classify_ingredients(foods: List[Food]) -> Tuple[List[str], Dict[str, List[str]]]:
    all_ingredients = []
    allergen_possibilities: Dict[str, List[str]] = {}
    for food in foods:
        for ingredient in food.ingredients:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)

    for food in foods:
        for allergen in food.allergens:
            if allergen in allergen_possibilities:
                current = allergen_possibilities[allergen]
                allergen_possibilities[allergen] = list(
                    set(food.ingredients).intersection(current)
                )
            else:
                allergen_possibilities[allergen] = food.ingredients

    possible_allergens = list(
        set(
            [
                possible_allergen
                for possible_allergens in allergen_possibilities.values()
                for possible_allergen in possible_allergens
            ]
        )
    )

    return (
        list(
            filter(
                lambda ingredient: ingredient not in possible_allergens,
                all_ingredients,
            )
        ),
        allergen_possibilities,
    )


def count_times_ingredients_appear(ingredients: List[str], foods: List[Food]) -> int:
    count = 0
    for food in foods:
        for ingredient in ingredients:
            if ingredient in food.ingredients:
                count += 1
    return count


def remove_ingredient(ingredient: str, allergen_dict: Dict[str, List[str]]):
    for allergen in allergen_dict:
        if ingredient in allergen_dict[allergen]:
            allergen_dict[allergen].remove(ingredient)


def reduce_possibilities(possible_allergen: Dict[str, List[str]]) -> Dict[str, str]:
    result: Dict[str, str] = {}

    while len(result) != len(possible_allergen):
        for allergen in possible_allergen:
            if len(possible_allergen[allergen]) == 1:
                ingredient = possible_allergen[allergen].pop()
                result[allergen] = ingredient
                remove_ingredient(ingredient, possible_allergen)
    return result


def sort_dict(d: Dict):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[0])}


def part1():
    foods = list(map(map_food, input.split("\n")))

    none_allergen, _ = classify_ingredients(foods)
    return count_times_ingredients_appear(none_allergen, foods)


def part2():
    foods = list(map(map_food, input.split("\n")))

    _, possible_allergen = classify_ingredients(foods)
    allergen_dict = reduce_possibilities(possible_allergen)
    allergen_dict = sort_dict(allergen_dict)

    return ",".join(allergen_dict.values())


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
