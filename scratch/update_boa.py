import re
import json

with open('frontend/src/data/curriculos/ele304.ts', 'r', encoding='utf-8') as f:
    text = f.read()

def get_block(start_str):
    start = text.find(start_str)
    if start == -1: return ""
    start = text.find('[', start)
    if start == -1: return ""
    stack = 0
    end = -1
    for i in range(start, len(text)):
        if text[i] == '[': stack += 1
        elif text[i] == ']':
            stack -= 1
            if stack == 0:
                end = i + 1
                break
    return text[start:end]

# For strings:
def get_str(key):
    m = re.search(f'{key}:\s*"([^"]+)"', text)
    if m: return m.group(1)
    return ""

familia = get_str('familia_profesional')
denominacion = get_str('denominacion')
nivel = get_str('nivel')
duracion = get_str('duracion')
ref = get_str('referente_europeo')

perfil = get_str('perfil_profesional')
comp_gen = get_str('competencia_general')

# Just run a simple regex for the rest or use simple text since we know the structure.
cpps = []
for m in re.finditer(r'\{ id:\s*"([^"]+)",\s*descripcion:\s*"([^"]+)"\s*\}', get_block('competencias_cpps')):
    cpps.append(f"{m.group(1)}) {m.group(2)}")

article_5 = "Competencias profesionales, personales y sociales.\n" + "\n".join(cpps)

boa_articles = {
  "article_2": f"El título de Técnico Superior en Sistemas de Telecomunicaciones e Informáticos queda identificado por los siguientes elementos:\nFamilia Profesional: {familia}\nDenominación: {denominacion}\nNivel: {nivel}\nDuración: {duracion}\nReferente Europeo: {ref}",
  "article_3": f"Perfil profesional del título.\n{perfil}",
  "article_4": f"Competencia general.\n{comp_gen}",
  "article_5": article_5,
  "article_6": "Cualificaciones y unidades de competencia.\nVer detalles en el currículo oficial.",
  "article_7": "Entorno profesional.\nVer detalles en el currículo oficial.",
  "article_8": "Prospectiva del título.\nVer detalles en el currículo oficial."
}

import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
cursor = conn.cursor()
cursor.execute("UPDATE degrees SET boa_articles=? WHERE code='ELE-23'", (json.dumps(boa_articles, ensure_ascii=False),))
conn.commit()
conn.close()
print("Updated boa_articles for ELE-23 successfully.")
