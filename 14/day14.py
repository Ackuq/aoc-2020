import re
import itertools
from typing import Dict


file = "input.txt"


def map_input(curr: str):
    split = curr.split(" = ")
    value = split[1]
    match = re.match(r"^([a-zA-Z]+)[\[]?(\d+)?[\]]?$", split[0])
    assert match is not None
    command = match.group(1)
    index = match.group(2)
    if index != None:
        return {"command": command, "index": index, "value": value}
    return {"command": command, "mask": value}


input = list(map(map_input, open("./{}".format(file)).read().split("\n")))


def sum_decimal(memory: Dict[int, int]):
    sum = 0
    for _, val in memory.items():
        sum += val
    return sum


def sum_binary(memory: Dict[int, str]):
    sum = 0
    for _, val in memory.items():
        sum += bin_to_dec(val)
    return sum


def bin_to_dec(bin):
    return int("0b{}".format(bin), 2)


def part1():
    def calculate(val: str, mask: str, use_floating=False):
        i = 0
        res = []
        assert len(val) == len(mask)
        for i in range(len(val)):
            if mask[i] == "X":
                res.append(val[i])
            else:
                res.append(mask[i])

            i += 1

        return "".join(res)

    mem: Dict[int, str] = {}

    current_mask = None
    for entry in input:
        if "mask" in entry:
            current_mask = entry.get("mask")
            continue
        decimal = entry.get("value")
        assert decimal is not None
        value = format(int(decimal), "036b")
        index = entry.get("index")
        assert current_mask is not None
        assert value is not None
        assert index is not None
        mem[int(index)] = calculate(value, current_mask)

    return sum_binary(mem)


def part2():
    mem: Dict[int, int] = {}

    def get_variations(address: str):
        no_floating = address.count("X")
        variations = list(itertools.product(*["01"] * no_floating))
        res = []
        for variation in variations:
            modified = address
            for i in variation:
                modified = modified.replace("X", i, 1)
            res.append(modified)
        return res

    def calculate_addresses(val: str, mask: str):
        i = 0
        res = []
        assert len(val) == len(mask)
        for i in range(len(val)):
            if mask[i] == "0":
                res.append(val[i])
            else:
                res.append(mask[i])

            i += 1

        return get_variations("".join(res))

    current_mask = None
    for entry in input:
        if "mask" in entry:
            current_mask = entry.get("mask")
            continue
        value = entry.get("value")
        address_decimal = entry.get("index")
        assert current_mask is not None
        assert value is not None
        assert address_decimal is not None
        for address in calculate_addresses(
            format(int(address_decimal), "036b"), current_mask
        ):
            mem[bin_to_dec(address)] = int(value)

    return sum_decimal(mem)


if __name__ == "__main__":
    print("Part 1: ", part1())
    print("Part 2: ", part2())
