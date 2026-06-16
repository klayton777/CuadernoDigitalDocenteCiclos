const fs = require('fs');

const { ELE304 } = require('../../frontend/src/data/curriculos/ele304.ts'); // Wait, require won't work on ts directly without ts-node

// Let's just generate the .cddp and .cddc using JSON files

// 1. We will extract RA and CE from ele304.ts
const content = fs.readFileSync('../../frontend/src/data/curriculos/ele304.ts', 'utf-8');

// The easiest way is to parse the TS as a string, but it's simpler to just write a python script that imports from DB!
