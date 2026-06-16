import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT id, degree_id, code, name FROM modules WHERE degree_id IN (SELECT id FROM degrees WHERE code IS NULL)")
for row in c.fetchall():
    print(row)
