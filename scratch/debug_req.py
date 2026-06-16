import requests
r = requests.get('http://localhost:8001/api/catalog/curriculum/ELE304')
print(r.status_code)
print(r.text)
