import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM degrees WHERE code IS NULL")
print('Null:', c.fetchone()[0])
c.execute("SELECT COUNT(*) FROM degrees WHERE code = ''")
print('Empty string:', c.fetchone()[0])
