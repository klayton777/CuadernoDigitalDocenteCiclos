import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT id, code, name FROM degrees WHERE code = 'ELE203'")
for row in c.fetchall():
    print(repr(row))
