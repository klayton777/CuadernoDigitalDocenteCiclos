import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

c.execute("SELECT id, name FROM degrees WHERE code = 'ELE203'")
degrees = c.fetchall()
print("ELE203 Degrees:", degrees)

for d in degrees:
    c.execute("SELECT COUNT(*) FROM modules WHERE degree_id = ?", (d[0],))
    print(f"Modules for ID {d[0]}:", c.fetchone()[0])

c.execute("SELECT id, name FROM degrees WHERE code = 'ELE304'")
degrees_304 = c.fetchall()
print("ELE304 Degrees:", degrees_304)

for d in degrees_304:
    c.execute("SELECT COUNT(*) FROM modules WHERE degree_id = ?", (d[0],))
    print(f"Modules for ID {d[0]}:", c.fetchone()[0])
