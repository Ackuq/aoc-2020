const fs = require("fs");

const input = fs
    .readFileSync("./input.txt")
    .toString()
    .split("\n")
    .map((entry) => {
        const re = /([a-zA-Z]+)([0-9]+)/;
        const match = entry.match(re);
        return { command: match[1], value: parseInt(match[2], 10) };
    });

const DIRECTIONS = {
    N: "N",
    E: "E",
    S: "S",
    W: "W",
};

const COMPASS = Object.keys(DIRECTIONS);

const COMMANDS = {
    F: "F",

    // Turning
    L: "L",
    R: "R",
};

const handleTurn = (oldDir, turn, degrees) => {
    const sign = turn === COMMANDS.R ? "+" : "-";
    const entryJumps = (degrees / 90) % 360;

    let newIndex = eval(
        `(${COMPASS.indexOf(oldDir)} ${sign} ${entryJumps}) % ${COMPASS.length}`
    );
    while (newIndex < 0) {
        newIndex += COMPASS.length;
    }

    return COMPASS[newIndex];
};

const driveBoat = (instructions, waypoint = null) => {
    let currentWaypoint = waypoint ? { ...waypoint } : null;
    const pos = COMPASS.reduce((prev, curr) => ({ ...prev, [curr]: 0 }), []);
    let currentDir = DIRECTIONS.E;

    instructions.forEach(({ command, value }) => {
        switch (command) {
            case COMMANDS.L:
            case COMMANDS.R:
                if (waypoint) {
                    const newWaypoint = {};
                    Object.keys(currentWaypoint).forEach((dir) => {
                        newWaypoint[handleTurn(dir, command, value)] =
                            currentWaypoint[dir];
                    });
                    currentWaypoint = newWaypoint;
                } else {
                    currentDir = handleTurn(currentDir, command, value);
                }
                break;
            case COMMANDS.F:
                if (waypoint) {
                    for (let i = 0; i < value; i++) {
                        Object.keys(pos).forEach((dir) => {
                            pos[dir] += currentWaypoint[dir];
                        });
                    }
                } else {
                    pos[currentDir] += value;
                }
                break;
            default:
                if (waypoint) {
                    currentWaypoint[command] += value;
                } else {
                    pos[command] += value;
                }
        }
    });

    return pos;
};

const manhattan = (pos) => {
    const [x, y] = [
        Math.abs(pos[DIRECTIONS.N] - pos[DIRECTIONS.S]),
        Math.abs(pos[DIRECTIONS.E] - pos[DIRECTIONS.W]),
    ];

    return x + y;
};

const part1 = () => {
    return manhattan(driveBoat(input));
};

console.log("Part 1: ", part1());

const part2 = () => {
    const waypoint = {
        [DIRECTIONS.N]: 1,
        [DIRECTIONS.E]: 10,
        [DIRECTIONS.S]: 0,
        [DIRECTIONS.W]: 0,
    };

    return manhattan(driveBoat(input, waypoint));
};

console.log("Part 2: ", part2());
