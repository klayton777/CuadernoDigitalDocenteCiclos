import sqlite3

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT code, COUNT(*) FROM degrees WHERE code IS NOT NULL GROUP BY code HAVING COUNT(*) > 1")
duplicates = c.fetchall()
print("Duplicated codes:")
for row in duplicates:
    print(row)
