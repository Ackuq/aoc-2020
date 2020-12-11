const fs = require("fs");

const input = fs
    .readFileSync("./input.txt")
    .toString()
    .split("\n")
    .map((row) => row.split(""));

const ELEMENTS = {
    EMPTY: "L",
    FLOOR: ".",
    OCCUPIED: "#",
};

const getNewMarker = (layout, row, column, visible, leaveThreshold) => {
    const current = layout[row][column];

    if (current === ELEMENTS.EMPTY) {
        if (visible.every((seat) => seat !== ELEMENTS.OCCUPIED)) {
            return ELEMENTS.OCCUPIED;
        }
    } else if (current === ELEMENTS.OCCUPIED) {
        if (
            visible.filter((seat) => seat === ELEMENTS.OCCUPIED).length >=
            leaveThreshold
        ) {
            return ELEMENTS.EMPTY;
        }
    }
    return current;
};

const countOccupied = (layout) => {
    let count = 0;
    layout.forEach((row) => {
        row.forEach((column) => {
            if (column === ELEMENTS.OCCUPIED) {
                count++;
            }
        });
    });
    return count;
};

const part1 = () => {
    const getAdjacent = (layout, row, column) => {
        const adjacent = [];

        for (
            let y = Math.max(row - 1, 0);
            y < Math.min(layout.length, row + 2);
            y++
        ) {
            for (
                let x = Math.max(column - 1, 0);
                x < Math.min(layout[y].length, column + 2);
                x++
            ) {
                if (y === row && x === column) {
                    continue;
                }
                adjacent.push(layout[y][x]);
            }
        }
        return adjacent;
    };

    const iterate = (oldLayout) => {
        const newLayout = JSON.parse(JSON.stringify(oldLayout));

        oldLayout.forEach((row, y) => {
            row.forEach((_, x) => {
                const adjacent = getAdjacent(oldLayout, y, x);
                newLayout[y][x] = getNewMarker(oldLayout, y, x, adjacent, 4);
            });
        });

        if (JSON.stringify(oldLayout) === JSON.stringify(newLayout)) {
            return [newLayout, false];
        }

        return [newLayout, true];
    };

    let layout = input,
        cont;
    do {
        [layout, cont] = iterate(layout);
    } while (cont);

    return countOccupied(layout);
};

console.log("Part 1: ", part1());

const part2 = () => {
    const getVisible = (layout, row, column) => {
        const visible = [];

        // Up negative
        for (let x = column - 1, y = row - 1; x >= 0 && y >= 0; x--, y--) {
            const element = layout[y][x];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        // Up positive
        for (
            let x = column + 1, y = row - 1;
            x < layout[0].length && y >= 0;
            x++, y--
        ) {
            const element = layout[y][x];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        // Down negative
        for (
            let x = column - 1, y = row + 1;
            x >= 0 && y < layout.length;
            x--, y++
        ) {
            const element = layout[y][x];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }
        // Down positive
        for (
            let x = column + 1, y = row + 1;
            x < layout[0].length && y < layout.length;
            x++, y++
        ) {
            const element = layout[y][x];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        // Up
        for (let y = row - 1; y >= 0; y--) {
            const element = layout[y][column];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        // Down
        for (let y = row + 1; y < layout.length; y++) {
            const element = layout[y][column];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        // Left
        for (let x = column - 1; x >= 0; x--) {
            const element = layout[row][x];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        // Right
        for (let x = column + 1; x < layout[0].length; x++) {
            const element = layout[row][x];
            if (element !== ELEMENTS.FLOOR) {
                visible.push(element);
                break;
            }
        }

        return visible;
    };

    const iterate = (oldLayout) => {
        const newLayout = JSON.parse(JSON.stringify(oldLayout));

        oldLayout.forEach((row, y) => {
            row.forEach((_, x) => {
                const visible = getVisible(oldLayout, y, x);
                newLayout[y][x] = getNewMarker(oldLayout, y, x, visible, 5);
            });
        });

        if (JSON.stringify(oldLayout) === JSON.stringify(newLayout)) {
            return [newLayout, false];
        }

        return [newLayout, true];
    };

    let layout = input,
        cont;
    do {
        [layout, cont] = iterate(layout);
    } while (cont);

    return countOccupied(layout);
};

console.log("Part 2: ", part2());
