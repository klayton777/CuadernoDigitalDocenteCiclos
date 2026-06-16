const fs = require('fs');

// We will read the TS file and extract the demoSeed string
const content = fs.readFileSync('frontend/src/services/demo-ele203-0237ictve-curso202526.ts', 'utf-8');

// Use regex or eval to get the object
const match = content.match(/export const demoSeed = (\{[\s\S]*\});\n$/);
if (match) {
    // evaluate it safely? No, it's safer to just remove the export and run it as JS
    const jsCode = content.replace('export const CRM_SEED_VERSION', 'const CRM_SEED_VERSION').replace('export const demoSeed', 'const demoSeed');
    
    // Evaluate it in a temporary file
    fs.writeFileSync('scratch/temp.js', jsCode + `\n
const cursoData = demoSeed['0237-ictve-curso-2025-26'];
cursoData.__version__ = 1;
fs.writeFileSync('0552-sirl-curso-2025-26.cddc', JSON.stringify(cursoData, null, 2), 'utf-8');
console.log('Generated 0552-sirl-curso-2025-26.cddc');
`);
}
