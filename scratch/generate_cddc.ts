import { demoSeed } from '../frontend/src/services/demo-ele203-0237ictve-curso202526.ts';
import fs from 'fs';

const cursoData = demoSeed['0237-ictve-curso-2025-26'];
// Just make sure it works as JSON, it's just an object.
cursoData.__version__ = 1;

fs.writeFileSync('0552-sirl-curso-2025-26.cddc', JSON.stringify(cursoData, null, 2), 'utf-8');
console.log('Generated 0552-sirl-curso-2025-26.cddc');
