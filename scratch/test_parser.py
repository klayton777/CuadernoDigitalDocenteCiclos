import urllib.request
from bs4 import BeautifulSoup
url = 'https://centrosdocentes.catedu.es/awc/modulo.php?cod=0525&ciclo=ELE304&horario=DIURNO&familia=ELE&nivel=CFGS'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
ra_cards = soup.find_all('div', class_='ra-card')
if ra_cards:
    for i, card in enumerate(ra_cards[:2]):
        header = card.find('div', class_='ra-header')
        print(f"--- RA {i+1} ---")
        if header: print("Header:", header.text.strip())
        
        ce_list = card.find('ul', class_='ce-list')
        if ce_list:
            ces = ce_list.find_all('li')
            for ce in ces[:2]:
                print("  CE:", ce.text.strip())
        else:
            print("No ce-list found")
else:
    print("No ra-card found")
