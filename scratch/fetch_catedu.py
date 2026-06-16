"""
Fetch RA/CE data for all ELE304 modules from CATEDU and generate a clean JSON.
Uses urllib since CATEDU returns plain HTML/text, not a SPA for individual modules.
"""
import urllib.request
import re
import json
import sys

# All 14 ELE304 module codes from BOA
ELE304_MODULES = ['0525', '0551', '0552', '0553', '0554', '0555', '0556', '0557', '0558', '0559', '0560', '0561', '0601', '0713']

BASE_URL = "https://centrosdocentes.catedu.es/awc/modulo.php?cod={cod}&ciclo=ELE304&horario=DIURNO&familia=ELE&nivel=CFGS"


def fetch_module(cod):
    url = BASE_URL.format(cod=cod)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        return html
    except Exception as e:
        print(f"  ERROR fetching {cod}: {e}", file=sys.stderr)
        return None


def clean_html(html):
    """Strip HTML tags and normalize whitespace."""
    text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    text = re.sub(r'<p[^>]*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<li[^>]*>', '\n• ', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def parse_module_html(html):
    """Extract module info and RA/CE from CATEDU HTML."""
    text = clean_html(html)
    
    # Extract module name from title
    title_match = re.search(r'#\s*\d+\.\s*(.+?)(?:\s*-\s*FP|$)', text)
    name = title_match.group(1).strip() if title_match else ""
    
    # Extract hours
    hours_match = re.search(r'Total:\s*(\d+)\s*horas', text)
    hours = int(hours_match.group(1)) if hours_match else 0
    
    # Extract course (1º or 2º)
    course_match = re.search(r'(\d)º\s*$', text, re.MULTILINE)
    course = f"{course_match.group(1)}º" if course_match else "1º"
    
    # Extract ECTS
    ects_match = re.search(r'([\d.]+)\s*Créditos?\s*ECTS', text)
    ects = float(ects_match.group(1)) if ects_match else 0
    
    # Extract RA/CE section
    ra_section = ""
    ra_start = text.find('Resultados de Aprendizaje')
    if ra_start == -1:
        ra_start = text.find('Resultados de aprendizaje')
    
    if ra_start >= 0:
        ra_section = text[ra_start:]
        # Remove any trailing footer/nav
        for end_marker in ['FP Aragón', 'Centros Docentes', 'Copyright', '©']:
            idx = ra_section.find(end_marker)
            if idx > 0:
                ra_section = ra_section[:idx]
    
    # Parse RA blocks: each RA ends with (RAx) and contains CEs
    ras = []
    # Split by RA pattern: text followed by (RAx)
    ra_blocks = re.split(r'\n\s*(.+?)\s*\(RA(\d+)\)', ra_section)
    
    # ra_blocks[0] is the header, then pairs of (description, ra_number)
    for i in range(1, len(ra_blocks), 2):
        ra_desc = ra_blocks[i].strip()
        ra_num = ra_blocks[i + 1].strip()
        
        if i + 2 < len(ra_blocks):
            ce_text = ra_blocks[i + 2].strip()
        else:
            ce_text = ""
        
        # Remove header text if present
        ra_desc = re.sub(r'^Resultados de [Aa]prendizaje.*', '', ra_desc).strip()
        
        # Parse CEs: they start with "Se ha..." or similar patterns
        ces = []
        ce_lines = re.split(r'\n', ce_text)
        ce_id = 1
        for line in ce_lines:
            line = line.strip()
            line = re.sub(r'^•\s*', '', line).strip()
            if not line:
                continue
            # Skip if it looks like the next section header
            if line.startswith('Contenidos') or line.startswith('Criterios generales'):
                break
            # Check if this looks like a CE (starts with "Se ha")
            if re.match(r'Se h[ae]', line):
                ces.append({
                    "id": f"CE{ra_num}.{ce_id}",
                    "descripcion": line.rstrip('.')
                })
                ce_id += 1
        
        if ra_desc:
            ras.append({
                "id": f"RA{ra_num}",
                "descripcion": ra_desc.rstrip('.'),
                "criterios_evaluacion": ces
            })
    
    return {
        "name": name,
        "hours": hours,
        "course": course,
        "ects": ects,
        "ra_count": len(ras),
        "ras": ras
    }


def main():
    results = {}
    
    for cod in ELE304_MODULES:
        print(f"Fetching {cod}...", file=sys.stderr)
        html = fetch_module(cod)
        if html:
            data = parse_module_html(html)
            results[cod] = data
            print(f"  -> {data['name']}: {data['hours']}h, {data['ra_count']} RAs, {data['course']}", file=sys.stderr)
        else:
            print(f"  FAILED", file=sys.stderr)
            results[cod] = None
    
    # Output JSON
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
