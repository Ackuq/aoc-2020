from functools import reduce
from enum import Enum
from typing import Any, Dict, List, Tuple, Union

file = "input"


class Keys(Enum):
    YOUR_TICKET = "your ticket:"
    NEARBY_TICKETS = "nearby tickets:"
    VALID = "valid"


def reduce_input(
    prev,
    curr: str,
):
    acc = prev.copy()
    rows = curr.split("\n")
    if rows[0] == Keys.YOUR_TICKET.value:
        rows.pop(0)
        my_tickets: List[int] = []
        for row in rows:
            my_tickets = my_tickets + list(map(int, row.split(",")))
        acc[Keys.YOUR_TICKET] = my_tickets
        return acc
    elif rows[0] == Keys.NEARBY_TICKETS.value:
        rows.pop(0)
        nearby_tickets: List[List[int]] = []
        for row in rows:
            nearby_tickets.append(list(map(int, row.split(","))))
        acc[Keys.NEARBY_TICKETS] = nearby_tickets
        return acc
    else:
        valid: List[List[Tuple[int, int]]] = []
        for row in rows:
            [_, value_string] = row.split(": ")
            intervals = value_string.split(" or ")
            values: List[Tuple[int, int]] = []
            for interval in intervals:
                [lower, higher] = interval.split("-")
                values.append((int(lower), int(higher)))
            valid.append(values)
        acc[Keys.VALID] = valid
        return acc


input: Dict[Keys, Any] = reduce(
    reduce_input,
    open("./{}.txt".format(file)).read().split("\n\n"),
    {Keys.VALID: {}},
)


def value_is_valid(value, intervals):
    for interval in intervals:
        if value >= interval[0] and value <= interval[1]:
            return True
    return False


def scan_tickets(tickets, valid):
    new_tickets = tickets.copy()
    invalid = []
    valid_intervals = [
        interval for interval_array in valid for interval in interval_array
    ]
    for ticket in tickets:
        for value in ticket:
            if not value_is_valid(value, valid_intervals):
                invalid.append(value)
                new_tickets.remove(ticket)
    return (new_tickets, invalid)


def part1():

    (_, invalid_values) = scan_tickets(input[Keys.NEARBY_TICKETS], input[Keys.VALID])
    return sum(invalid_values)


def part2():
    (new_tickets, _) = scan_tickets(input[Keys.NEARBY_TICKETS], input[Keys.VALID])

    def sort_notes(tickets, valid):
        mapping: Dict[int, Tuple[int, List[int]]] = {}
        valid_enumerated = list(enumerate(valid))
        tickets_enumerated = list(enumerate(zip(*tickets)))

        while len(mapping) < len(valid):
            for interval_index, intervals in valid_enumerated:
                valid_elements = []
                for i, values in tickets_enumerated:
                    if all(value_is_valid(value, intervals) for value in values):
                        valid_elements.append((i, values))

                if len(valid_elements) == 1:
                    element = valid_elements.pop()
                    tickets_enumerated.remove(element)
                    valid_enumerated.remove((interval_index, intervals))
                    mapping[interval_index] = element
        return mapping

    mapping = sort_notes(new_tickets, input[Keys.VALID])

    your_ticket = input[Keys.YOUR_TICKET]
    values = [your_ticket[mapping[i][0]] for i in range(6)]

    return reduce((lambda x, y: x * y), values)


print("Part 1:", part1())
print("Part 2:", part2())
