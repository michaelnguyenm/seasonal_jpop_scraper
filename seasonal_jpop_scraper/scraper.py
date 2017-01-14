from bs4 import BeautifulSoup # Used to parse xml/html
from urllib.parse import urlparse # Parses URL to get path
import os.path
import urllib.request # Requests XML that has been compressed
import gzip
from datetime import datetime # Used to format datetime for mongodb
import time # Limit the number of requests

# Based on: http://stackoverflow.com/questions/7894384/
def get_adb_id(adb_link):
    """
    Function info
    """
    url = urlparse(adb_link)
    path = url.path
    split_path = os.path.split(path)
    temp_id = split_path[1]
    return temp_id[1:]

# Based on: https://gist.github.com/Manouchehri/0ce55d239fb07c41c92f
def get_adb_airdate(adb_id):
    """
    Function info
    """
    time.sleep(3)
    url = 'http://api.anidb.net:9001/httpapi?request=anime&client=seasonaljpop&clientver=1&protover=1&aid=' + adb_id
    header = {'Accept-Encoding' : 'gzip'}
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    data = gzip.decompress(response.read())
    soup = BeautifulSoup(data, 'html.parser')
    date = soup.startdate.contents[0]
    return date

# Date given in string form
# Based on: http://stackoverflow.com/questions/23581128/
def formatted_airdate(date):
    """
    Function info
    """
    for fmt in ('%Y', '%Y-%m', '%Y-%m-%d'):
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('Date does not match formats expected')

def main():
    # Consider not hardcoding the file from the local directory
    soup = BeautifulSoup(open('anime.html'), 'html.parser')

    # interactive python3, use exec(open('scraper.py').read())
    title_tag_list = soup.find_all('h3')
    for line in title_tag_list:
        # Entire tag
        # print(line)
        # Just the contents of the tag
        # print(line.contents)

        # from http://stackoverflow.com/questions/2612548/
        # Get names
        title_jp = line.get('data-japanese')
        title_rom = line.get('data-romaji')
        title_en = line.get('data-english')
        title_other = line.get('data-alternate')

        # Get links
        # Need to make tests for when these classes don't exist
        mal_link = line.find_next('a', {'class':'mal-icon'}).get('href')
        adb_link = line.find_next('a', {'class':'anidb-icon'}).get('href')

        # Get airdate
        # Process link for ID
        adb_id = get_adb_id(adb_link)
        airdate = None
        # Look up ID on anidb if it exists
        if (adb_id != ''):
            unformatted_airdate = get_adb_airdate(adb_id) # 1970-01-01 is none, incomplete will not have all info
            # Process date string
            if (unformatted_airdate != '1970-01-01'):
                airdate = formatted_airdate(unformatted_airdate)
        # Add to anime database
        # Find music
        # Add to music database

if __name__ == '__main__':
    main()
