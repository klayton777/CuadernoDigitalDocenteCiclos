import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

# Modules without RA - full list
c.execute('''
    SELECT m.code, m.name, d.code as degree_code, d.name as degree_name
    FROM modules m
    JOIN degrees d ON m.degree_id = d.id
    WHERE m.id NOT IN (SELECT DISTINCT module_id FROM learning_outcomes)
    ORDER BY d.code, m.code
''')
no_ra = c.fetchall()
print(f'MODULES WITHOUT RA: {len(no_ra)}')
print()

# Group by degree
from collections import defaultdict
by_degree = defaultdict(list)
for r in no_ra:
    by_degree[r[2]].append(r)

for degree_code in sorted(by_degree.keys()):
    modules = by_degree[degree_code]
    print(f'{degree_code} ({modules[0][3]}): {len(modules)} modules without RA')
    for m in modules:
        print(f'  {m[0]} {m[1]}')

conn.close()
