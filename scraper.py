from bs4 import BeautifulSoup

# consider not hardcoding the file
soup = BeautifulSoup(open('test.html'), 'html.parser')

# interactive python3, use exec(open('scraper.py').read())

for line in soup.find_all('h3'):
    # print(line.contents)
    # from http://stackoverflow.com/questions/2612548/extracting-an-attribute-value-with-beautifulsoup
    print(line.get('data-japanese'))
    print(line.get('data-romaji'))
    print(line.get('data-english'))
    print(line.get('data-alternate'))
