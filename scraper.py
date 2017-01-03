from bs4 import BeautifulSoup

soup = BeautifulSoup(open('test.html'), 'html.parser')

# interactive python3, use exec(open('scraper.py').read())

for line in soup.find_all('h3'):
    # print(line.contents)
    print(line.get('data-japanese'))
    print(line.get('data-romaji'))
    print(line.get('data-english'))
    print(line.get('data-alternate'))
