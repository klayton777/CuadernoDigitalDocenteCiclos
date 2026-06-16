import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

c.execute("SELECT id, code, name FROM degrees WHERE code = 'ELE203'")
print("ELE203 Degrees:")
for row in c.fetchall():
    print(row)
    
    # Check modules for this degree
    c.execute("SELECT id, code, name FROM modules WHERE degree_id = ?", (row[0],))
    mods = c.fetchall()
    print(f"  -> {len(mods)} modules")
    for m in mods:
        print(f"     Module: {m[1]} - {m[2]}")

conn.close()
