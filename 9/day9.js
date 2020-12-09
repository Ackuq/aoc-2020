const fs = require("fs");

const input = fs
    .readFileSync("./input.txt")
    .toString()
    .split("\n")
    .map((num) => parseInt(num, 10));

const PREAMBLE_LENGTH = 25;

let previous = [];

const isValid = (num, prev) => {
    for (let i = 0; i < prev.length - 1; i++) {
        for (let j = i + 1; j < prev.length; j++) {
            if (prev[i] + prev[j] === num) {
                return true;
            }
        }
    }
    return false;
};

let index = 0;
while (index < PREAMBLE_LENGTH) {
    previous.push(input[index]);
    index++;
}

const getFirstInvalid = () => {
    while (index < input.length) {
        const curr = input[index];
        if (isValid(curr, previous)) {
            previous.shift();
            previous.push(curr);
        } else {
            return curr;
        }
        index++;
    }
};

const invalid = getFirstInvalid();

console.log(`Part 1: ${invalid}`);

const iterate = (rest, current, goal, memo) => {
    const element = rest[0];
    const next = element + current;
    const newMemo = [...memo, element];
    if (next === goal) {
        return newMemo;
    } else if (next < goal) {
        const res = iterate(rest.slice(1), next, goal, newMemo);
        if (res) {
            return res;
        }
    }
};

const getSubset = () => {
    for (let i = 0; i < input.length - 1; i++) {
        const element = input[i];
        const res = iterate(input.slice(i + 1), element, invalid, [element]);

        if (res) {
            return res;
        }
    }
};

const subset = getSubset();

console.log(`Part 2: ${Math.min(...subset) + Math.max(...subset)}`);
