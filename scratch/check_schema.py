import sqlite3
import json

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]

schema = {}
for t in tables:
    c.execute(f"PRAGMA table_info({t})")
    schema[t] = [r[1] for r in c.fetchall()]

print(json.dumps(schema, indent=2))
