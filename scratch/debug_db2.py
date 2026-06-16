import sqlite3
import requests

conn = sqlite3.connect('backend/cdd_pro.db')
c = conn.cursor()
c.execute("SELECT id, code, name FROM degrees WHERE code LIKE '%ELE203%'")
for row in c.fetchall():
    print("DB Degree:", repr(row))

print("Fetching from API...")
try:
    r = requests.get('http://localhost:8000/api/catalog/curriculum/ELE203')
    print("API status:", r.status_code)
    print("API response:", r.text)
except Exception as e:
    print(e)
