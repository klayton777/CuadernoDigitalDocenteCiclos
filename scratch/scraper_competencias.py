import sqlite3
import urllib.request
import urllib.parse
import json
import time

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

c.execute("SELECT DISTINCT code FROM modules")
modules = [row[0] for row in c.fetchall()]
print(f"Encontrados {len(modules)} modulos distintos.")

url = 'https://centrosdocentes.catedu.es/awc/public/competencias/api/tab4_convalidar_modulos.php'
updated = 0

for code in modules:
    data = urllib.parse.urlencode({'accion': 'calcular_competencias_necesarias', 'modulo': code}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode('utf-8'))
            if resp_data.get('success'):
                grupos = resp_data['data'].get('grupos_competencias', [])
                if grupos:
                    grupos_json = json.dumps(grupos, ensure_ascii=False)
                    c.execute("UPDATE modules SET convalidation_competences = ? WHERE code = ?", (grupos_json, code))
                    updated += 1
                    if updated % 10 == 0:
                        conn.commit()
    except Exception as e:
        print(f"Error procesando el modulo {code}: {e}")
        time.sleep(0.5)

conn.commit()
print(f"Hecho. Modulos actualizados con competencias: {updated}")
conn.close()
