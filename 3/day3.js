const fs = require("fs");

const inputBuffer = fs.readFileSync("./input.txt");

const input = inputBuffer.toString().split("\n");

const getTrees = ({ xSlope, ySlope }) => {
  let x = xSlope,
    y = ySlope,
    trees = 0;

  while (y < input.length) {
    if (input[y][x % input[y].length] === "#") {
      trees++;
    }
    x += xSlope;
    y += ySlope;
  }
  return trees;
};

console.log(`Part 1: ${getTrees({ xSlope: 3, ySlope: 1 })}`);

const slopesToCheck = [
  { xSlope: 1, ySlope: 1 },
  { xSlope: 3, ySlope: 1 },
  { xSlope: 5, ySlope: 1 },
  { xSlope: 7, ySlope: 1 },
  { xSlope: 1, ySlope: 2 },
];

const slopeTress = slopesToCheck.map((slope) => getTrees(slope));

const res = slopeTress.reduce((prev, curr) => prev * curr, 1);

console.log(`Part 2: ${res}`);
