import sqlite3
import urllib.request
import json
import time
from bs4 import BeautifulSoup
import re

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            print(f"Error fetching {url}: {e}, retrying...")
            time.sleep(2)
    return None

def get_html(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching {url}: {e}, retrying...")
            time.sleep(2)
    return None

def run_scraper():
    conn = sqlite3.connect('backend/cdd_pro.db')
    c = conn.cursor()
    
    print("Fetching Families...")
    familias_data = get_json('https://centrosdocentes.catedu.es/awc/api/get_familias.php')
    if not familias_data or familias_data.get('status') != 'success':
        print("Failed to get familias")
        return
        
    for fam in familias_data['data']:
        code = fam['codfamilia']
        name = fam['familia']
        
        # Skip weird or empty families if necessary
        if not code: continue
            
        c.execute("INSERT OR IGNORE INTO professional_families (code, name) VALUES (?, ?)", (code, name))
        conn.commit()
        
        c.execute("SELECT id FROM professional_families WHERE code = ?", (code,))
        family_id = c.fetchone()[0]
        
        print(f"Processing Family {code}: {name}")
        
        levels = ['CFGB', 'CFGM', 'CFGS', 'CE']
        for level in levels:
            url_ciclos = f"https://centrosdocentes.catedu.es/awc/api/get_ciclos.php?codfamilia={code}&nivel={level}"
            ciclos_data = get_json(url_ciclos)
            if not ciclos_data or ciclos_data.get('status') != 'success':
                continue
                
            for ciclo in ciclos_data['data']:
                codciclo = ciclo['codciclo']
                ciclo_name = ciclo['ciclo']
                db_level = "BASICA" if level == "CFGB" else "MEDIO" if level == "CFGM" else "SUPERIOR" if level == "CFGS" else "ESPECIALIZACION"
                
                c.execute("INSERT OR IGNORE INTO degrees (family_id, level, name, code) VALUES (?, ?, ?, ?)", 
                         (family_id, db_level, ciclo_name, codciclo))
                conn.commit()
                
                c.execute("SELECT id FROM degrees WHERE code = ?", (codciclo,))
                degree_id = c.fetchone()[0]
                
                url_info_ciclo = f"https://centrosdocentes.catedu.es/awc/api/get_info_ciclo.php?codciclo={codciclo}"
                info_ciclo = get_json(url_info_ciclo)
                if not info_ciclo or info_ciclo.get('status') != 'success':
                    continue
                    
                modulos = info_ciclo['data'].get('modulos', [])
                for mod in modulos:
                    codmodulo = mod['codmodulo']
                    modulo_name = mod['modulo']
                    horas = mod.get('horas') or 0
                    
                    curso_raw = mod.get('curso')
                    curso_db = "1º"
                    if curso_raw == 1: curso_db = "1º"
                    elif curso_raw == 2: curso_db = "2º"
                    elif curso_raw is None: curso_db = "Ambos"
                    else: curso_db = str(curso_raw) + "º"
                    
                    c.execute("INSERT OR IGNORE INTO modules (degree_id, code, name, hours, curso) VALUES (?, ?, ?, ?, ?)",
                             (degree_id, codmodulo, modulo_name, horas, curso_db))
                    conn.commit()
                    
                    c.execute("UPDATE modules SET name = ?, hours = ?, curso = ? WHERE degree_id = ? AND code = ?", 
                             (modulo_name, horas, curso_db, degree_id, codmodulo))
                    conn.commit()
                    
                    c.execute("SELECT id FROM modules WHERE degree_id = ? AND code = ?", (degree_id, codmodulo))
                    module_id = c.fetchone()[0]
                    
                    c.execute("SELECT COUNT(*) FROM learning_outcomes WHERE module_id = ?", (module_id,))
                    if c.fetchone()[0] > 0:
                        continue
                        
                    print(f"    - Scraping module {codmodulo}: {modulo_name}")
                    url_mod = f"https://centrosdocentes.catedu.es/awc/modulo.php?cod={codmodulo}&ciclo={codciclo}&familia={code}&nivel={level}"
                    html = get_html(url_mod)
                    if not html:
                        continue
                        
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    ra_cards = soup.find_all('div', class_='ra-card')
                    if not ra_cards:
                        continue
                        
                    for i, card in enumerate(ra_cards):
                        header = card.find('div', class_='ra-header')
                        if not header:
                            continue
                        
                        # Remove the "(RAx)" text at the end using regex
                        ra_text_full = header.text.strip()
                        ra_text = re.sub(r'\s*\(RA\d+\)$', '', ra_text_full).strip()
                        
                        ra_number = i + 1
                        c.execute("INSERT INTO learning_outcomes (module_id, ra_number, description) VALUES (?, ?, ?)",
                                 (module_id, ra_number, ra_text))
                        conn.commit()
                        ra_id = c.lastrowid
                        
                        ce_list = card.find('ul', class_='ce-list')
                        if ce_list:
                            for li in ce_list.find_all('li'):
                                ce_lines = li.text.strip().split('\n')
                                if not ce_lines: continue
                                ce_code = ce_lines[0].strip()
                                ce_desc = " ".join([l.strip() for l in ce_lines[1:] if l.strip()])
                                # Sometimes ce_code might be missing the letter
                                if not ce_code.endswith(')'):
                                    # Fallback
                                    ce_code = f"CE{ra_number}.x"
                                    ce_desc = li.text.strip()
                                
                                c.execute("INSERT INTO evaluation_criteria (learning_outcome_id, ce_code, description) VALUES (?, ?, ?)",
                                         (ra_id, ce_code, ce_desc))
                            conn.commit()
                    time.sleep(0.5)

    print("Scraping completed!")
    conn.close()

if __name__ == '__main__':
    run_scraper()
