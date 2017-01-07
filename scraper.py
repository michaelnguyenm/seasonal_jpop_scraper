from bs4 import BeautifulSoup

# Consider not hardcoding the file from the local directory
soup = BeautifulSoup(open('anime.html'), 'html.parser')

# interactive python3, use exec(open('scraper.py').read())
title_tags_list = soup.find_all('h3')
for line in title_tag_list:
    # Entire tag
    # print(line)
    # Just the contents of the tag
    # print(line.contents)
    # from http://stackoverflow.com/questions/2612548/extracting-an-attribute-value-with-beautifulsoup
    # Get names
    title_jp = line.get('data-japanese')
    title_rom = line.get('data-romaji')
    title_en = line.get('data-english')
    title_other = line.get('data-alternate')
    # Get air date
    # Get MAL link
    mal_link = line.find_next('a', {'class':'mal-icon'}).get('href')
