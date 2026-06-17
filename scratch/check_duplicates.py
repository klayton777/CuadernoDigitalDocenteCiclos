import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

# How many degrees total?
c.execute('SELECT COUNT(*) FROM degrees')
total_degrees = c.fetchone()[0]
print(f'Total degrees: {total_degrees}')

# How many modules per degree on average?
c.execute('SELECT COUNT(*) FROM modules')
total_modules = c.fetchone()[0]
print(f'Total modules: {total_modules}')
print(f'Average modules per degree: {total_modules / total_degrees:.1f}')

# Check: how many degrees have modules?
c.execute('SELECT COUNT(DISTINCT degree_id) FROM modules')
degrees_with_modules = c.fetchone()[0]
print(f'Degrees with modules: {degrees_with_modules}')

# Check: degrees WITHOUT modules
c.execute('''
    SELECT d.id, d.code, d.name 
    FROM degrees d 
    LEFT JOIN modules m ON d.id = m.degree_id 
    WHERE m.id IS NULL
    ORDER BY d.code
''')
no_modules = c.fetchall()
print(f'\nDegrees WITHOUT modules ({len(no_modules)}):')
for r in no_modules:
    print(f'  id={r[0]} | {r[1]} | {r[2]}')

# Check: modules per degree distribution
c.execute('''
    SELECT d.code, d.name, COUNT(m.id) as module_count
    FROM degrees d
    JOIN modules m ON d.id = m.degree_id
    GROUP BY d.id
    ORDER BY module_count DESC
    LIMIT 10
''')
print('\nTop 10 degrees by module count:')
for r in c.fetchall():
    print(f'  {r[0]} | {r[1]} | {r[2]} modules')

# Check: modules with RA/CE vs without
c.execute('''
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN ra_count > 0 THEN 1 ELSE 0 END) as with_ra,
        SUM(CASE WHEN ra_count = 0 THEN 1 ELSE 0 END) as without_ra
    FROM (
        SELECT m.id, 
            (SELECT COUNT(*) FROM learning_outcomes lo WHERE lo.module_id = m.id) as ra_count
        FROM modules m
    )
''')
r = c.fetchone()
print(f'\nModules with RA: {r[1]}/{r[0]}')
print(f'Modules without RA: {r[2]}/{r[0]}')

# Check: how many RA/CE per module (sample)
c.execute('''
    SELECT m.code, m.name, d.code as degree_code,
        (SELECT COUNT(*) FROM learning_outcomes lo WHERE lo.module_id = m.id) as ra_count,
        (SELECT COUNT(*) FROM evaluation_criteria ec 
         JOIN learning_outcomes lo2 ON ec.learning_outcome_id = lo2.id 
         WHERE lo2.module_id = m.id) as ce_count
    FROM modules m
    JOIN degrees d ON m.degree_id = d.id
    WHERE m.code IN ('1708', '1709', '1710', '1665', '0179', '1713', '1664', '0156')
    ORDER BY m.code, d.code
''')
rows = c.fetchall()
print(f'\nRA/CE counts for transversal modules ({len(rows)} rows):')
for r in rows:
    print(f'  {r[0]} {r[1][:40]:40s} | degree={r[2]:10s} | RA={r[3]} CE={r[4]}')

# Summary per transversal module
from collections import defaultdict
summary = defaultdict(lambda: {'count': 0, 'with_ra': 0, 'without_ra': 0, 'ra_counts': set()})
for r in rows:
    summary[r[0]]['count'] += 1
    if r[3] > 0:
        summary[r[0]]['with_ra'] += 1
        summary[r[0]]['ra_counts'].add(r[3])
    else:
        summary[r[0]]['without_ra'] += 1

print('\n=== TRANSVERSAL MODULE SUMMARY ===')
for code in sorted(summary.keys()):
    s = summary[code]
    ra_vals = sorted(s['ra_counts'])
    print(f'  {code}: {s["count"]} copies | {s["with_ra"]} with RA | {s["without_ra"]} without RA | RA counts: {ra_vals}')

# Modules without RA
c.execute('''
    SELECT m.code, m.name, d.code as degree_code
    FROM modules m
    JOIN degrees d ON m.degree_id = d.id
    WHERE m.id NOT IN (SELECT DISTINCT module_id FROM learning_outcomes)
    ORDER BY d.code, m.code
''')
no_ra = c.fetchall()
print(f'\n=== MODULES WITHOUT RA ({len(no_ra)}) ===')
for r in no_ra[:30]:
    print(f'  {r[2]:10s} | {r[0]} {r[1]}')
if len(no_ra) > 30:
    print(f'  ... and {len(no_ra) - 30} more')

conn.close()
