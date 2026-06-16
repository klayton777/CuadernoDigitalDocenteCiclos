import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

c.execute("SELECT id FROM degrees WHERE code = 'ELE-23'")
old_id = c.fetchone()[0]

c.execute("SELECT id FROM degrees WHERE code = 'ELE304'")
new_id = c.fetchone()[0]

# Delete the empty new ID
c.execute("DELETE FROM degrees WHERE id = ?", (new_id,))

# Update old ID to correct code
c.execute("UPDATE degrees SET code = 'ELE304', name = 'Sistemas de Telecomunicaciones e Informáticos' WHERE id = ?", (old_id,))

conn.commit()
print("Fixed ELE-23 -> ELE304")

# Look for any other '-' degrees
c.execute("SELECT code, name FROM degrees WHERE code LIKE '%-%'")
print("Remaining hyphens:")
for row in c.fetchall():
    print(repr(row))

conn.close()
