const { assert } = require("console");
const fs = require("fs");

const buffer = fs.readFileSync("./input.txt");

const inputArray = buffer.toString().split("\n");

// Last element is blank
inputArray.pop();

const pairs = [];
const triples = [];

const arrayEqual = (_arr1) => (_arr2) => {
  const arr1 = _arr1.sort();
  const arr2 = _arr2.sort();

  return JSON.stringify(arr1) === JSON.stringify(arr2);
};

for (let i = 0; i < inputArray.length; i++) {
  const first = parseInt(inputArray[i]);

  for (let j = 0; j < inputArray.length; j++) {
    if (i === j) {
      continue;
    }
    const second = parseInt(inputArray[j]);
    if (first + second === 2020) {
      // We already found the pair
      if (pairs.some(arrayEqual([i, j]))) {
        continue;
      }
      pairs.push([i, j]);
    }

    for (let k = 0; k < inputArray.length; k++) {
      if (i === k || j === k) {
        continue;
      }
      const third = parseInt(inputArray[k]);

      if (first + second + third === 2020) {
        // We already found the triple
        if (triples.some(arrayEqual([i, j, k]))) {
          continue;
        }

        triples.push([i, j, k]);
      }
    }
  }
}

assert(pairs.length === 1);
assert(triples.length === 1);

pairs.forEach((pair) => {
  const first = inputArray[pair[0]];
  const second = inputArray[pair[1]];
  console.log(`${first} * ${second} = ${first * second}`);
});

triples.forEach((triple) => {
  const first = inputArray[triple[0]];
  const second = inputArray[triple[1]];
  const third = inputArray[triple[2]];
  console.log(`${first} * ${second} * ${third} = ${first * second * third}`);
});
