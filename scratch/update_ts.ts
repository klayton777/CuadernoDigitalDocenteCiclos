import { ELE304 } from '../frontend/src/data/curriculos/ele304';
import { ELE203 } from '../frontend/src/data/curriculos/ele203';
import * as fs from 'fs';

const stiModules = JSON.parse(fs.readFileSync('scratch/sti_modules.json', 'utf-8'));
const itModules = JSON.parse(fs.readFileSync('scratch/it_modules.json', 'utf-8'));

for (const mod of ELE304.modulos) {
    const parsedMod = stiModules.find(m => m.codigo === mod.codigo);
    if (parsedMod && parsedMod.resultados_aprendizaje.length > 0) {
        mod.resultados_aprendizaje = parsedMod.resultados_aprendizaje;
    }
}

for (const mod of ELE203.modulos) {
    const parsedMod = itModules.find(m => m.codigo === mod.codigo);
    if (parsedMod && parsedMod.resultados_aprendizaje.length > 0) {
        mod.resultados_aprendizaje = parsedMod.resultados_aprendizaje;
    }
}

const ele304Content = `import type { CurriculumTitulo } from "./index";

export const ELE304: CurriculumTitulo = ${JSON.stringify(ELE304, null, 2)};
`;

const ele203Content = `import type { CurriculumTitulo } from "./index";

export const ELE203: CurriculumTitulo = ${JSON.stringify(ELE203, null, 2)};
`;

fs.writeFileSync('frontend/src/data/curriculos/ele304.ts', ele304Content, 'utf-8');
fs.writeFileSync('frontend/src/data/curriculos/ele203.ts', ele203Content, 'utf-8');

console.log('Successfully updated ele304.ts and ele203.ts');
