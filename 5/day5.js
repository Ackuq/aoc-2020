const fs = require("fs");

const inputBuffer = fs.readFileSync("./input.txt");

const boardingPasses = inputBuffer.toString().split("\n");

const HIGH_ROW = "B";

const calcRow = (rowString) => {
  let row = 0;
  for (let i = 0; i < rowString.length; i++) {
    row +=
      Math.pow(2, rowString.length - 1 - i) *
      (rowString[i] === HIGH_ROW ? 1 : 0);
  }
  return row;
};

const HIGH_SEAT = "R";

const calcSeat = (seatString) => {
  let seat = 0;
  for (let i = 0; i < seatString.length; i++) {
    seat +=
      Math.pow(2, seatString.length - 1 - i) *
      (seatString[i] === HIGH_SEAT ? 1 : 0);
  }
  return seat;
};

const passIDs = [];

boardingPasses.forEach((pass) => {
  const row = calcRow(pass.slice(0, 7));
  const seat = calcSeat(pass.slice(7, 10));
  const passID = row * 8 + seat;
  passIDs.push(passID);
});

const sortedIDs = passIDs.sort((a, b) => a - b);
const maxID = sortedIDs[sortedIDs.length - 1];

console.log(`Part 1: ${maxID}`);

for (let i = 0; i < sortedIDs.length - 1; i++) {
  const curr = sortedIDs[i];
  const next = sortedIDs[i + 1];
  if (next !== curr + 1) {
    console.log(`Part 2: ${curr + 1}`);
  }
}
