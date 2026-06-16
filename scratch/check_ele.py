import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT code, name FROM degrees WHERE code LIKE '%ELE%' OR name LIKE '%ELE%'")
for row in c.fetchall():
    print(repr(row))
