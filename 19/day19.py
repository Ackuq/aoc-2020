import re
from functools import reduce
from typing import Dict, List, Tuple, Union

file_name = "example2"

input = open("./{}.txt".format(file_name)).read()


def reduce_rules(prev, rule: str):
    [key, value] = rule.split(": ")

    char = re.match(r"^\"([a-zA-Z]).*\"$", value)
    if char is not None:
        prev[int(key)] = char.group(1)
    else:
        if "|" in value:
            options = map(lambda a: list(map(int, a.split(" "))), value.split(" | "))
            prev[int(key)] = tuple(options)
        else:
            prev[int(key)] = list(map(int, value.split(" ")))

    return prev


[rules, messages] = input.split("\n\n")

rules = reduce(reduce_rules, rules.split("\n"), {})
messages = messages.split("\n")


def expand_rule(rule, rule_index, part2: bool):
    if part2:
        if rule_index == 8:
            expanded42 = expand_rule(rules[42], 42, part2)
            return ["(", expanded42, ")+"]

        if rule_index == 11:
            expanded42 = expand_rule(rules[42], 42, part2)
            expanded31 = expand_rule(rules[31], 31, part2)
            ret = reduce(
                lambda prev, i: prev
                + [
                    "(",
                    expanded42,
                    ")(",
                    expanded42,
                    "){" + str(i) + "}(",
                    expanded31,
                    "){" + str(i) + "}",
                ],
                range(1, 3),
                [],
            )
            return ret

    if isinstance(rule, str):
        return rule
    elif isinstance(rule, list):
        result = []

        for index in rule:
            if index != rule_index:
                result.append(expand_rule(rules[index], index, part2))

        # If lowest level reduce to string
        if all(isinstance(s, str) for s in result):
            return "".join(result)

        return result
    elif isinstance(rule, tuple):
        result = []
        for option in rule:
            expanded = expand_rule(option, rule_index, part2)
            if all(isinstance(s, str) for s in expanded):
                result.append("".join(expanded))

            else:
                result.append(expanded)
        return tuple(result)
    else:
        print("Warning: Unknown rule type:", type(rule))
    return []


def create_possible_strings(rule) -> Union[List[str], str]:
    if isinstance(rule, str):
        return rule
    elif isinstance(rule, list):
        combinations = []
        for sub_rule in rule:
            new = []
            new_combinations = create_possible_strings(sub_rule)
            for new_combination in new_combinations:
                if len(combinations) == 0:
                    new.append(new_combination)
                else:
                    for combination in combinations:
                        new.append(combination + new_combination)

            combinations = new
        return combinations
    return ""


def possible_strings(rule):
    result = []

    if isinstance(rule, str):
        return rule

    elif isinstance(rule, list):
        for sub_rule in rule:
            if isinstance(sub_rule, str):
                if len(result) == 0:
                    result.append(sub_rule)
                else:
                    new_result = []
                    for res in result:
                        new_result.append(res + sub_rule)
                    result = new_result
            else:
                options = possible_strings(sub_rule)
                new_result = []
                for option in options:
                    if len(result) == 0:
                        new_result.append(option)
                    else:
                        for combination in result:
                            new_result.append(combination + option)

                result = new_result
    elif isinstance(rule, tuple):
        new_result = []
        for option in rule:
            a = possible_strings(option)
            if isinstance(a, list):
                for b in a:
                    if len(result) == 0:
                        new_result.append(b)
                    else:
                        for combination in result:
                            new_result.append(combination + b)

            else:
                if len(result) == 0:
                    new_result.append(a)
                else:
                    for combination in result:
                        new_result.append(combination + a)

        result = new_result

    return result


def part1():
    rule = expand_rule(rules[0], 0, True)
    print("RULES DONE")
    possible = possible_strings(rule)
    count = 0
    for message in messages:
        matches = list(
            filter(
                lambda a: a is not None,
                map(lambda b: re.match("^{}$".format(b), message), possible),
            )
        )
        if len(matches) == 1:
            match = matches.pop()
            print(match.group())
            count += 1
        elif len(matches) > 1:
            print("HANDLE THIS")
    return count


if __name__ == "__main__":
    print("Part 1:", part1())
