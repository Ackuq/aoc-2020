const fs = require("fs");

const adapters = fs
    .readFileSync("./input.txt")
    .toString()
    .split("\n")
    .map((num) => parseInt(num, 10))
    .sort((a, b) => a - b);

// Input text = adapter output joltage
// Any adapter can take [output - 3, output] as input
// Built in joltage = max(adapters) + 3

const myJoltage = Math.max(...adapters) + 3;

adapters.push(myJoltage);

/* Part 1 */

const part1 = () => {
    const iterate = (current, rest, memo) => {
        const choices = rest.filter(
            (num) => num - current >= 1 && num - current <= 3
        );

        for (let i = 0; i < choices.length; i++) {
            const element = choices[i];
            const indexToRemove = rest.indexOf(element);
            const newRest = [
                ...rest.slice(0, indexToRemove),
                ...rest.slice(indexToRemove + 1),
            ];

            const newMemo = [...memo, element - current];
            if (newRest.length === 0) {
                return newMemo;
            } else {
                const res = iterate(element, newRest, newMemo);
                if (res) {
                    return res;
                }
            }
        }
    };

    const result = iterate(0, adapters, []).reduce((prev, curr) => {
        if (curr in prev) {
            return { ...prev, [curr]: prev[curr] + 1 };
        } else {
            return { ...prev, [curr]: 1 };
        }
    }, {});

    return result[1] * result[3];
};

console.log(`Part 1: ${part1()}`);

const part2 = () => {
    const iterate = (current, rest, memo) => {
        const choices = rest.filter(
            (num) => num - current >= 1 && num - current <= 3
        );

        let solutions = 0;
        let currMemo = memo;

        for (let i = 0; i < choices.length; i++) {
            const element = choices[i];

            if (element in memo) {
                solutions += memo[element];
                continue;
            }

            if (element === myJoltage) {
                solutions += 1;
                continue;
            }

            const indexToRemove = rest.indexOf(element);
            const newRest = [
                ...rest.slice(0, indexToRemove),
                ...rest.slice(indexToRemove + 1),
            ];

            let [newSolutions, newMemo] = iterate(element, newRest, currMemo);
            solutions += newSolutions;
            currMemo = newMemo;
        }

        return [solutions, { ...currMemo, [current]: solutions }];
    };

    return iterate(0, adapters, []);
};

console.log(`Part 2: ${part2()}`);
