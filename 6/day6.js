const fs = require("fs");

const inputBuffer = fs.readFileSync("./input.txt");

const answers = inputBuffer
  .toString()
  .split("\n\n")
  .map((group) => group.split("\n"));

let total = 0;

answers.forEach((group) => {
  let unique = [];

  group.forEach((individual) => {
    for (let i = 0; i < individual.length; i++) {
      const element = individual[i];
      if (!unique.includes(element)) {
        unique.push(element);
      }
    }
  });

  total += unique.length;
});

console.log(`Part 1: ${total}`);

total = 0;

answers.forEach((group) => {
  let answerMap = {};

  group.forEach((individual) => {
    for (let i = 0; i < individual.length; i++) {
      const element = individual[i];
      if (element in answerMap) {
        answerMap[element] = answerMap[element] + 1;
      } else {
        answerMap[element] = 1;
      }
    }
  });
  for (const entries of Object.values(answerMap)) {
    if (entries === group.length) {
      total++;
    }
  }
});

console.log(`Part 2: ${total}`);
