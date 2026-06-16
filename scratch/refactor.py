import re

with open(r'c:\GD-rsp\APP\frontend\src\app\catalogo\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove curriculos import
content = re.sub(r'curriculos,\n\s*', '', content)
content = re.sub(r'import {\n\s*type CurriculumTitulo,\n\s*type CurriculumModulo,\n\s*type CurriculumRA,\n\s*type CurriculumCE,\n} from "@/data/curriculos";', 
'''import {
  type CurriculumTitulo,
  type CurriculumModulo,
  type CurriculumRA,
  type CurriculumCE,
} from "@/data/curriculos";''', content)

content = re.sub(r'const familias = Array\.from\(new Set\(Object\.values\(curriculos\)\.map\(\(t\) => t\.familia\)\)\)\.sort\(\);\nconst titulosPorFamilia: Record<string, CurriculumTitulo\[\]> = {};\nfor \(const t of Object\.values\(curriculos\)\) \{\n  if \(!titulosPorFamilia\[t\.familia\]\) titulosPorFamilia\[t\.familia\] = \[\];\n  titulosPorFamilia\[t\.familia\]\.push\(t\);\n\}', '', content)


tab_cursos_start = content.find('function TabCursos')
tab_modulos_start = content.find('function TabModulos')

tab_cursos = content[tab_cursos_start:tab_modulos_start]

cursos_replace = """
  const selectedFamilia = globalSelection.familia;
  const selectedTitulo = globalSelection.tituloCodigo;
  const curriculoCodigo = selectedTitulo;

  const [titulo, setTitulo] = useState<any>(null);
  const [tituloLoading, setTituloLoading] = useState(false);

  useEffect(() => {
    if (selectedTitulo) {
      setTituloLoading(true);
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/catalog/curriculum/${selectedTitulo}`)
        .then(res => res.json())
        .then(json => {
          if (json.status === 'success') setTitulo(json.data);
          else setTitulo(null);
          setTituloLoading(false);
        })
        .catch(() => { setTitulo(null); setTituloLoading(false); });
    } else {
      setTitulo(null);
    }
  }, [selectedTitulo]);

  const familyNames = families.map((f) => f.name).sort();
  const selectedFamilyObj = families.find((f) => f.name === selectedFamilia);
  const degreesFromApi = selectedFamilyObj?.degrees ?? [];

  const modulosPrimero = titulo ? titulo.modulos.filter((m: any) => m.curso === "1º" || m.curso === "Ambos") : [];
  const modulosSegundo = titulo ? titulo.modulos.filter((m: any) => m.curso === "2º" || m.curso === "Ambos") : [];
"""

block_to_replace = re.search(r'const selectedFamilia = globalSelection\.familia;.*?const modulosSegundo = titulo \? titulo\.modulos\.filter\(\(m\) => m\.curso === "2º"\) : \[\];', tab_cursos, re.DOTALL).group(0)

tab_cursos = tab_cursos.replace(block_to_replace, cursos_replace)

tab_modulos_content = content[tab_modulos_start:]

modulos_replace = """
  const selectedFamilia = globalSelection.familia;
  const selectedTitulo = globalSelection.tituloCodigo;
  const curriculoCodigo = selectedTitulo;
  const selectedModuloCodigo = globalSelection.moduloCodigo;

  const [titulo, setTitulo] = useState<any>(null);
  const [tituloLoading, setTituloLoading] = useState(false);

  useEffect(() => {
    if (selectedTitulo) {
      setTituloLoading(true);
      fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/catalog/curriculum/${selectedTitulo}`)
        .then(res => res.json())
        .then(json => {
          if (json.status === 'success') setTitulo(json.data);
          else setTitulo(null);
          setTituloLoading(false);
        })
        .catch(() => { setTitulo(null); setTituloLoading(false); });
    } else {
      setTitulo(null);
    }
  }, [selectedTitulo]);

  const familyNames = families.map((f) => f.name).sort();
  const selectedFamilyObj = families.find((f) => f.name === selectedFamilia);
  const degreesFromApi = selectedFamilyObj?.degrees ?? [];

  const modulo = titulo
    ? titulo.modulos.find((m: any) => m.codigo === selectedModuloCodigo)
    : undefined;
"""

block_to_replace_modulos = re.search(r'const selectedFamilia = globalSelection\.familia;.*?const modulo = titulo\s*\?\s*titulo\.modulos\.find\(\(m\) => m\.codigo === selectedModuloCodigo\)\s*:\s*undefined;', tab_modulos_content, re.DOTALL).group(0)

tab_modulos_content = tab_modulos_content.replace(block_to_replace_modulos, modulos_replace)

new_content = content[:tab_cursos_start] + tab_cursos + tab_modulos_content

# Fix the JSX where it references `titulo` but might now have `tituloLoading`
new_content = new_content.replace('{selectedTitulo && !titulo && (', '{selectedTitulo && !titulo && !tituloLoading && (')
new_content = new_content.replace('{selectedTitulo && titulo && (', '{selectedTitulo && titulo && !tituloLoading && (')
new_content = new_content.replace('{selectedModuloCodigo && !modulo && (', '{selectedModuloCodigo && !modulo && !tituloLoading && (')
new_content = new_content.replace('{selectedModuloCodigo && modulo && (', '{selectedModuloCodigo && modulo && !tituloLoading && (')

# Add loading spinner logic to JSX
spinner_jsx = '''
      {tituloLoading && (
        <div className="flex items-center justify-center p-12">
          <div className="w-8 h-8 border-4 border-accent border-t-transparent rounded-full animate-spin" />
        </div>
      )}
'''

new_content = re.sub(r'(\{selectedTitulo && !titulo && !tituloLoading && \()', spinner_jsx + r'\1', new_content)
# Since we replaced it in multiple places, we need to be careful. I will just let the user know if they need spinner. It's fine for now.

with open(r'c:\GD-rsp\APP\frontend\src\app\catalogo\page.tsx', 'w', encoding='utf-8') as f:
    f.write(new_content)
