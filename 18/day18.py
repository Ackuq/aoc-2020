from typing import List, Union


file_name = "input"

input = open("./{}.txt".format(file_name)).read()


def map_expressions(row: str) -> List[str]:
    expressions = []
    current_expression = ""
    parenthesis = 0
    for char in row:
        if char == "(":
            if parenthesis > 0:
                current_expression += char
            parenthesis += 1
        elif char == ")":
            parenthesis -= 1
            if parenthesis == 0:
                expressions.append(map_expressions(current_expression))
                current_expression = ""
            else:
                current_expression += char
        elif parenthesis != 0:
            current_expression += char
        elif char != " ":
            expressions.append(char)

    return expressions


list_input = list(map(map_expressions, input.split("\n")))


def evaluate_expression(expression):
    result = None
    current_sign = None
    for sub_expression in expression:
        if sub_expression == "+" or sub_expression == "-" or sub_expression == "*":
            current_sign = sub_expression
        else:
            value = None
            if isinstance(sub_expression, list):
                value = evaluate_expression(sub_expression)
            else:
                value = sub_expression

            if result is None:
                result = value
            else:
                result = eval("{} {} {}".format(result, current_sign, value))
    return result


def part1():

    sum = 0
    for expression in list_input:
        sum += evaluate_expression(expression)

    return sum


def part2():
    def evaluate_addition(expression):
        result = []
        current_sign = None
        for sub_expression in expression:
            if sub_expression == "+" or sub_expression == "-" or sub_expression == "*":
                current_sign = sub_expression
            else:
                value = None
                if isinstance(sub_expression, list):
                    value = evaluate_expression(evaluate_addition(sub_expression))
                else:
                    value = sub_expression

                if len(result) == 0:
                    result.append(value)
                elif current_sign == "+":
                    result[-1] = eval(
                        "{} {} {}".format(result[-1], current_sign, value)
                    )
                else:

                    result.append(current_sign)
                    result.append(value)
        return result

    sum = 0
    for expression in list_input:
        sum += evaluate_expression(evaluate_addition(expression))

    return sum


if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
