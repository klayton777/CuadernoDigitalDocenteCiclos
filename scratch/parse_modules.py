import re
import json

def parse_boa_text(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    modules = []
    parts = re.split(r'Módulo [pP]rofesional\s*:', text)
    
    for part in parts[1:]:
        match_code = re.search(r'Código\s*:\s*(\d{4})', part, re.IGNORECASE)
        if not match_code:
            continue
        codigo = match_code.group(1)
        
        name_part = part[:match_code.start()].strip()
        name = re.sub(r'[\r\n]+', ' ', name_part).strip(' .')
        
        ra_start = part.find('Resultados de aprendizaje y criterios de evaluación')
        if ra_start == -1:
            continue
            
        ra_end = part.find('Contenidos', ra_start)
        if ra_end == -1:
            ra_end = len(part)
            
        ra_section = part[ra_start:ra_end]
        
        # Remove the header first so we don't split on it!
        ra_section = re.sub(r'Resultados de aprendizaje y criterios de evaluación\s*:?', '', ra_section, count=1, flags=re.IGNORECASE)
        
        ras = []
        
        ra_blocks = re.split(r'Criterios de evaluación\s*:', ra_section, flags=re.IGNORECASE)
        
        if len(ra_blocks) > 1:
            ra_desc = ra_blocks[0].strip()
            ra_desc = re.sub(r'^\d+\.\s*', '', ra_desc).strip()
            
            for i in range(1, len(ra_blocks)):
                block = ra_blocks[i].strip()
                
                # Split by likely CE starts, e.g. "Se han", "Se ha", "a)", "- "
                # However, there are no newlines in the raw text sometimes!
                # Wait, "Se han" is usually capitalized. We can split by (?=Se h[a-z])
                # Let's split the block into lines first, or if there are no lines, split by "Se h" but carefully.
                # In STI, the text looks like "Se han identificado los elementos...Se han identificado el conjunto..."
                # There are NO newlines between CEs in some PDFs!
                # Let's split by regex: (?=Se h[a-z]{1,2}\s) or (?=[a-z]\)\s)
                # But wait, the next RA starts with a capital letter, e.g., "Configura infraestructuras..."
                # How to distinguish next RA from a CE?
                # CEs usually start with "Se " or lowercase letter + ")".
                # Next RA usually starts with an imperative verb (e.g. "Configura", "Monta", "Verifica", "Mantiene").
                
                # Let's split by (?=[A-Z]) to find sentences.
                sentences = re.split(r'(?<=\.)(?=[A-Z])', block)
                if len(sentences) <= 1:
                    sentences = re.split(r'(?<=\.)\s+(?=[A-Z])', block)
                
                ces = []
                next_ra_desc = []
                
                for s in sentences:
                    s = s.strip()
                    if not s: continue
                    
                    if re.match(r'^([a-z]\)|[-•]|Se\s|A\s|De\s|El\s|La\s|Los\s|Las\s|En\s)', s, re.IGNORECASE):
                        # Wait, what if the next RA starts with "Se..."? RA usually starts with 3rd person singular verb.
                        # We will assume if we haven't hit something clearly NOT a CE, it's a CE.
                        if len(next_ra_desc) == 0:
                            ces.append(s)
                        else:
                            next_ra_desc.append(s)
                    else:
                        # Might be the next RA. If it doesn't start with "Se ", we assume it's next RA.
                        # Wait, sometimes CE is "Realiza..." or "Dibuja...".
                        # But wait, usually CEs are "Se ha...". If it starts with "Se ha", it's a CE.
                        # Let's use a simpler heuristic: if it starts with "Se h", it's a CE.
                        if s.startswith('Se h') or re.match(r'^[a-z]\)', s):
                            if len(next_ra_desc) == 0:
                                ces.append(s)
                            else:
                                next_ra_desc.append(s)
                        else:
                            # Not starting with 'Se h', so it is probably the next RA!
                            next_ra_desc.append(s)
                
                # Fallback: if we didn't find any "Se h", just put everything except last sentence in CEs.
                if len(ces) == 0 and len(next_ra_desc) > 0:
                    ces = next_ra_desc[:-1]
                    next_ra_desc = next_ra_desc[-1:] if len(next_ra_desc) > 0 else []

                formatted_ces = []
                for j, ce_text in enumerate(ces):
                    ce_text = re.sub(r'^[a-z]\)\s*', '', ce_text).strip()
                    ce_text = re.sub(r'^[-•]\s*', '', ce_text).strip()
                    if ce_text:
                        formatted_ces.append({
                            "id": f"CE{len(ras)+1}.{j+1}",
                            "descripcion": ce_text
                        })
                
                if ra_desc:
                    ras.append({
                        "id": f"RA{len(ras)+1}",
                        "descripcion": ra_desc,
                        "criterios_evaluacion": formatted_ces
                    })
                
                ra_desc = " ".join(next_ra_desc).strip()
                ra_desc = re.sub(r'^\d+\.\s*', '', ra_desc).strip()
                
        modules.append({
            "codigo": codigo,
            "nombre": name,
            "horas": 0,
            "curso": "1º",
            "resultados_aprendizaje": ras
        })
        
    return modules

sti_modules = parse_boa_text('boa_sti_extracted.txt')
it_modules = parse_boa_text('boa_it_extracted.txt')

for m in sti_modules:
    print('STI', m['codigo'], len(m['resultados_aprendizaje']))
for m in it_modules:
    print('IT ', m['codigo'], len(m['resultados_aprendizaje']))

with open('scratch/sti_modules.json', 'w', encoding='utf-8') as f:
    json.dump(sti_modules, f, ensure_ascii=False, indent=2)

with open('scratch/it_modules.json', 'w', encoding='utf-8') as f:
    json.dump(it_modules, f, ensure_ascii=False, indent=2)
