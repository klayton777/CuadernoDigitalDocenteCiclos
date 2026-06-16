import sqlite3
import json
import os

db_path = 'backend/cdd_pro.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Fetch RA
cursor.execute("SELECT id_ra, desc_ra, peso_ra FROM learning_outcome_items WHERE module_document_id='Programacion_SIRL'")
ras = cursor.fetchall()

# 2. Fetch CE
cursor.execute("SELECT id_ce, id_ra, id_ud, desc_ce, peso_ce FROM evaluation_criterion_items WHERE module_document_id='Programacion_SIRL'")
ces = cursor.fetchall()

conn.close()

# 3. Create df_ra
df_ra = []
for ra in ras:
    df_ra.append({
        "RA": ra[0],
        "Descripción": ra[1],
        "Peso (%)": float(ra[2]) if ra[2] else 0.0,
        "Trimestre": "1T",
        "Horas": 0
    })

# 4. Create df_ce
df_ce = []
for ce in ces:
    df_ce.append({
        "CE": ce[0],
        "Descripción": ce[3],
        "RA": ce[1],
        "Peso (%)": float(ce[4]) if ce[4] else 0.0,
        "FEOE": False,
        "UD": ce[2] if ce[2] else "UD01",
        "Competencia Vinculada": "",
        "OG Vinculado": ""
    })

# 5. Get demo seed to copy df_ud, info_modulo, etc.
# Wait, let's just make a very basic df_ud
df_ud = [
    {
        "UD": "UD01",
        "Título": "Introducción a SIRL",
        "Trimestre": "1T",
        "Horas": 20,
        "Descripción": "Introducción",
        "Objetivos": ""
    }
]

# We will export this as 0552-sirl-pd.cddp
pd_data = {
    "__version__": 1,
    "tipo": "programacion",
    "info_modulo": {
        "codigo": "0552",
        "nombre": "Sistemas informáticos y redes locales",
        "horas": 160,
        "curso": "1º",
        "especialidad_profesorado": "Sistemas y Aplicaciones Informáticas",
        "tipo_modulo": "Profesional",
        "descripcion": "Gestión, administración y mantenimiento de sistemas informáticos y redes locales."
    },
    "df_ra": df_ra,
    "df_ce": df_ce,
    "df_ud": df_ud
}

with open('0552-sirl-pd.cddp', 'w', encoding='utf-8') as f:
    json.dump(pd_data, f, ensure_ascii=False, indent=2)

print("Generated 0552-sirl-pd.cddp")

