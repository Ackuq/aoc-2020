const fs = require("fs");

const rules = fs.readFileSync("./input.txt").toString().split("\n");

const MY_BAG = "shiny gold";

const rulesMap = {};

for (let i = 0; i < rules.length; i++) {
  const rule = rules[i];
  const [bag, rest] = rule.split(" contain ");
  let contain = [];
  if (rest !== "no other bags.") {
    contain = rest.split(", ").map((contain) => {
      const number = parseInt(contain.match(/^[0-9]+/)[0]);
      const containBag = contain
        .replace(`${number} `, "")
        .replace(/bags|bag\b/g, "")
        .replace(".", "")
        .trimEnd();
      return { bag: containBag, number };
    });
  }
  rulesMap[bag.replace("bags", "").trimEnd()] = contain;
}
// First task
let found = [];

let currentConnected = [MY_BAG];
let nextConnected = [];
let shouldContinue;

do {
  shouldContinue = false;
  for (const [bag, contains] of Object.entries(rulesMap)) {
    const connected = contains.filter((contain) =>
      currentConnected.includes(contain.bag)
    );
    if (connected.length > 0) {
      found.push(bag);
      nextConnected.push(bag);
      shouldContinue = true;
    }
  }
  currentConnected = nextConnected;
  nextConnected = [];
} while (shouldContinue);

// Filter duplicates
found = found.filter((item, index) => found.indexOf(item) === index);
console.log(`Part 1: ${found.length}`);

// Second task

let bags = 0;
let currentBags = [MY_BAG];
let nextBags = [];

do {
  currentBags.forEach((bag) => {
    const contains = rulesMap[bag];
    contains.forEach((contain) => {
      for (let i = 0; i < contain.number; i++) {
        bags++;
        nextBags.push(contain.bag);
      }
    });
  });
  currentBags = nextBags;
  nextBags = [];
} while (currentBags.length > 0);

console.log(`Part 2: ${bags}`);
