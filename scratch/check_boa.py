import sqlite3
conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT length(boa_articles) FROM degrees WHERE id = 137")
print('BOA Articles length:', c.fetchone()[0])
