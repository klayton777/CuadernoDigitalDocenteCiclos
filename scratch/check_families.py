import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

# Get column names for key tables
for table in ['professional_families', 'degrees', 'modules', 'learning_outcomes', 'evaluation_criteria']:
    c.execute(f'PRAGMA table_info({table})')
    cols = [r[1] for r in c.fetchall()]
    print(f'{table}: {cols}')

print()

# Check for duplicate families
c.execute('SELECT code, COUNT(*) as cnt FROM professional_families GROUP BY code HAVING cnt > 1')
dupes = c.fetchall()
print('=== DUPLICATE family codes ===')
for d in dupes:
    print(f'  {d}')
if not dupes:
    print('  (none)')

c.execute('SELECT COUNT(*) FROM professional_families')
print(f'Total familias: {c.fetchone()[0]}')

c.execute('SELECT id, code, name FROM professional_families ORDER BY code')
for row in c.fetchall():
    print(f'  id={row[0]} | {row[1]} | {row[2]}')

# Check for duplicate degrees
print('\n=== DUPLICATE degree codes ===')
c.execute('SELECT code, COUNT(*) as cnt FROM degrees GROUP BY code HAVING cnt > 1')
dupes2 = c.fetchall()
for d in dupes2:
    print(f'  {d}')
if not dupes2:
    print('  (none)')

c.execute('SELECT COUNT(*) FROM degrees')
print(f'Total grados: {c.fetchone()[0]}')

# Check for duplicate modules
print('\n=== DUPLICATE module codes ===')
c.execute('SELECT code, COUNT(*) as cnt FROM modules GROUP BY code HAVING cnt > 1')
dupes3 = c.fetchall()
for d in dupes3:
    print(f'  {d}')
if not dupes3:
    print('  (none)')

c.execute('SELECT COUNT(*) FROM modules')
print(f'Total modulos: {c.fetchone()[0]}')

# Check learning_outcomes and evaluation_criteria counts
print('\n=== RA / CE counts ===')
c.execute('SELECT COUNT(*) FROM learning_outcomes')
print(f'Total RA: {c.fetchone()[0]}')
c.execute('SELECT COUNT(*) FROM evaluation_criteria')
print(f'Total CE: {c.fetchone()[0]}')

conn.close()
