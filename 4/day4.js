const fs = require("fs");

const inputBuffer = fs.readFileSync("./input.txt");

const expectedFields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];

const passports = inputBuffer
  .toString()
  .split("\n\n")
  .map((passport) => passport.split(/\s+/))
  .map((passport) =>
    passport.reduce((prev, curr) => {
      const [key, value] = curr.split(":");
      return { ...prev, [key]: value };
    }, {})
  );

let valid = 0;

passports.forEach((passport) => {
  const keys = Object.keys(passport);
  if (expectedFields.every((expected) => keys.includes(expected))) {
    valid++;
  }
});

console.log(`Part 1: ${valid}`);

const COLOR_REGEX = /^#[0-9a-f]{6}$/i;
const PID_REGEX = /^[0-9]{9}$/i;

const EYE_COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];

const checkValidity = (passport) => {
  const keys = Object.keys(passport);
  if (!expectedFields.every((expected) => keys.includes(expected))) {
    return false;
  }
  const byr = parseInt(passport[expectedFields[0]]);
  const iyr = parseInt(passport[expectedFields[1]]);
  const eyr = parseInt(passport[expectedFields[2]]);
  const hgt = passport[expectedFields[3]];
  const hcl = passport[expectedFields[4]];
  const ecl = passport[expectedFields[5]];
  const pid = passport[expectedFields[6]];

  const hgtUnit = hgt.substr(hgt.length - 2, hgt.length - 1);
  const hgtValue = parseInt(hgt.split(hgtUnit)[0]);

  if (byr < 1920 || byr > 2002) {
    return false;
  }

  if (iyr < 2010 || iyr > 2020) {
    return false;
  }

  if (eyr < 2020 || eyr > 2030) {
    return false;
  }

  if (hgtUnit === "in") {
    if (hgtValue < 59 || hgtValue > 76) {
      return false;
    }
  } else if (hgtUnit === "cm") {
    if (hgtValue < 150 || hgtValue > 193) {
      return false;
    }
  } else {
    return false;
  }

  if (!hcl.match(COLOR_REGEX)) {
    return false;
  }

  if (!EYE_COLORS.some((color) => ecl === color)) {
    return false;
  }

  if (!pid.match(PID_REGEX)) {
    return false;
  }

  return true;
};

valid = 0;

passports.forEach((passport) => {
  if (checkValidity(passport)) {
    valid++;
  }
});

console.log(`Part 2: ${valid}`);
