const fs = require("fs");

const buffer = fs.readFileSync("./input.txt");

const inputArray = buffer.toString().split("\n");

let valid = 0;

inputArray.forEach((input) => {
  const elements = input.split(" ");

  const interval = elements[0].split("-");
  const char = elements[1][0];
  const password = elements[2];

  const re = new RegExp(`[^${char}]`, "g");
  const filtered = password.replace(re, "");
  const len = filtered.length;
  if (len >= parseInt(interval[0]) && len <= parseInt(interval[1])) {
    valid++;
  }
});

console.log(`Fulfills interval: ${valid}`);

valid = 0;

inputArray.forEach((input) => {
  const elements = input.split(" ");

  const positions = elements[0].split("-");
  const char = elements[1][0];
  const password = elements[2];

  const first = password[parseInt(positions[0]) - 1];
  const second = password[parseInt(positions[1]) - 1];

  if (first !== second) {
    if (first === char || second === char) {
      valid++;
    }
  }
});

console.log(`Fulfills positions: ${valid}`);
