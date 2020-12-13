const fs = require("fs");

const input = fs
    .readFileSync("./input.txt")
    .toString()
    .split("\n")
    .map((row, index) => {
        if (index === 0) {
            return parseInt(row, 10);
        } else {
            return row.split(",").map((el) => {
                // Only contains digits
                if (el.match(/^[0-9]+$/) !== null) {
                    return parseInt(el);
                }
                return el;
            });
        }
    });

const part1 = () => {
    const getEarliestDeparture = (earliest, ids) => {
        let currentTime = earliest;
        while (true) {
            for (let i = 0; i < ids.length; i++) {
                if (ids[i] === "x") {
                    continue;
                }
                if (currentTime % ids[i] === 0) {
                    return [ids[i], currentTime];
                }
            }
            currentTime++;
        }
    };

    const [busId, earliestDeparture] = getEarliestDeparture(input[0], input[1]);
    return busId * (earliestDeparture - input[0]);
};

console.log("Part 1: ", part1());

const part2 = () => {
    const chineseRemainder = (list) => {
        // Multiplicative inverse of a under modulo m
        const getInverse = (a, m) => {
            let m0 = m;
            let x0 = BigInt(0),
                x1 = BigInt(1);
            if (m === 1) {
                return 1;
            }
            while (a > 1) {
                // q is quotient
                let q = BigInt(a / m);

                let temp = m;

                // m is remainder now, process
                // same as Euclid's algo
                m = a % m;
                a = temp;

                temp = x0;

                // Update x0 and x1
                x0 = x1 - q * x0;
                x1 = temp;
            }
            if (x1 < 0) {
                x1 += m0;
            }
            return x1;
        };

        let sum = BigInt(0);
        let prod = BigInt(1);
        for (let i = 0; i < list.length; i++) {
            prod *= list[i].bus;
        }

        list.forEach(({ bus, offset }) => {
            const p = BigInt(prod / bus);
            sum += BigInt(offset * getInverse(p, bus) * p);
            console.log(sum);
        });
        return sum % prod;
    };

    const busOffset = [];

    for (let i = 0; i < input[1].length; i++) {
        if (input[1][i] !== "x") {
            busOffset.push({
                bus: BigInt(input[1][i]),
                offset: BigInt(input[1][i] - i),
            });
        }
    }

    return chineseRemainder(busOffset);
};

console.log("Part 2: ", part2());
