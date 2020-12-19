import re
from functools import reduce
from typing import SupportsAbs

file_name = "input"
PART2 = True


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


input = open("./{}.txt".format(file_name)).read()

[rules, messages] = input.split("\n\n")

rules = reduce(reduce_rules, rules.split("\n"), {})
messages = messages.split("\n")


def generate_regex(rule, index, part2):
    if part2:
        if index == 8:
            return "({})+".format(generate_regex(rules[42], 42, part2))
        elif index == 11:
            regex42 = generate_regex(rules[42], 42, part2)
            regex31 = generate_regex(rules[31], 31, part2)
            result = map(
                lambda i: "{}{{{}}}{}{{{}}}".format(regex42, i, regex31, i),
                range(1, 10),
            )
            return "({})".format("|".join(result))

    result = ""
    if isinstance(rule, str):
        return rule
    elif isinstance(rule, list):
        for rule_index in rule:
            result += generate_regex(rules[rule_index], rule_index, part2)
    elif isinstance(rule, tuple):
        options = []
        for sub_rule in rule:
            options.append(generate_regex(sub_rule, -1, part2))
        result = "({})".format("|".join(options))

    return result


if __name__ == "__main__":
    regex = re.compile("^{}$".format(generate_regex(rules[0], 0, PART2)))
    count = 0

    for message in messages:
        if regex.match(message):
            count += 1

    print(count)
