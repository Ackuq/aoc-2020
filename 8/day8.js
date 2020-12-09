const { assert } = require("console");
const fs = require("fs");
const { exit } = require("process");

const input = fs
    .readFileSync("./input.txt")
    .toString()
    .split("\n")
    .map((curr) => curr.split(" "));

const commands = {
    nop: "nop",
    jmp: "jmp",
    acc: "acc",
};

let acc = 0;
let rowIndex = 0;

let visitedRows = [];

const execute = (row) => {
    const command = row[0];
    const match = row[1].match(/(\+|\-)([0-9]*)/);

    const sign = match[1];
    const value = match[2];

    switch (command) {
        case commands.acc:
            acc = eval(`${acc} ${sign} ${value}`);
            rowIndex++;
            break;
        case commands.jmp:
            rowIndex = eval(`${rowIndex} ${sign} ${value}`);
            break;
        case commands.nop:
            rowIndex++;
            break;
    }
};

while (rowIndex < input.length) {
    if (visitedRows.includes(rowIndex)) {
        break;
    } else {
        visitedRows.push(rowIndex);
    }
    execute(input[rowIndex]);
}

console.log(`Part 1: ${acc}`);

acc = 0;
rowIndex = 0;

visitedRows = [];

const fixCommand = (row) => {
    const [oldCommand, ...rest] = row;
    if (oldCommand === commands.jmp) {
        return [commands.nop, ...rest];
    } else if (oldCommand === commands.nop) {
        return [commands.jmp, ...rest];
    } else {
        console.error("Command to fix wasn't jump nor nop");
        exit(1);
    }
};

let fixedRow = -1;

const fixRow = () => {
    if (fixedRow !== -1) {
        input[fixedRow] = fixCommand(input[fixedRow]);
    }
    for (let i = fixedRow + 1; i < input.length; i++) {
        if (input[i][0] === commands.jmp || input[i][0] === commands.nop) {
            fixedRow = i;
            input[fixedRow] = fixCommand(input[fixedRow]);
            break;
        }
    }
};

while (rowIndex < input.length) {
    if (visitedRows.includes(rowIndex)) {
        fixRow();
        visitedRows = [];
        rowIndex = 0;
        acc = 0;
    } else {
        visitedRows.push(rowIndex);
    }

    execute(input[rowIndex]);
}

console.log(`Part 2: ${acc}`);
