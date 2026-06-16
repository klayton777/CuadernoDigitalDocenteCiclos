import urllib.request
import json
req = urllib.request.Request('http://127.0.0.1:8001/api/catalog/curriculum/ELE304', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        for m in data['data']['modulos']:
            print(f"{m['codigo']} - {m['nombre']} - {m['horas']}h")
except Exception as e:
    print('Error:', e)
