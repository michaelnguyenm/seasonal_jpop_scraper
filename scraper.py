from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os.path
import time

#
def get_adb_id(adb_link):
    url = urlparse(adb_link)
    path = url.path
    sliced_path = os.path.split(path)
    temp_id = sliced_path[1]
    return temp_id[1:]

# Consider not hardcoding the file from the local directory
soup = BeautifulSoup(open('anime.html'), 'html.parser')

# interactive python3, use exec(open('scraper.py').read())
title_tag_list = soup.find_all('h3')
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
    # Get links
    # Need to make tests for when these classes don't exist
    mal_link = line.find_next('a', {'class':'mal-icon'}).get('href')
    adb_link = line.find_next('a', {'class':'anidb-icon'}).get('href')
    # Process link for ID
    adb_id = get_adb_id(adb_link)
    # Look up ID on anidb if it exists
