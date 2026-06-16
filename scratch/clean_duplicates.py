import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()

c.execute("SELECT code, COUNT(*) FROM degrees WHERE code IS NOT NULL GROUP BY code HAVING COUNT(*) > 1")
duplicates = c.fetchall()

deleted_count = 0
for row in duplicates:
    code = row[0]
    c.execute("SELECT id FROM degrees WHERE code = ?", (code,))
    ids = [r[0] for r in c.fetchall()]
    
    # Check which one has modules
    for deg_id in ids:
        c.execute("SELECT COUNT(*) FROM modules WHERE degree_id = ?", (deg_id,))
        count = c.fetchone()[0]
        if count == 0:
            c.execute("DELETE FROM degrees WHERE id = ?", (deg_id,))
            deleted_count += 1
            print(f"Deleted duplicate degree ID {deg_id} for code {code}")

conn.commit()
print(f"Total deleted: {deleted_count}")
conn.close()
