from bs4 import BeautifulSoup # Used to parse xml/html
from urllib.parse import urlparse # Parses URL to get path
import os.path
import urllib.request # Requests XML that has been compressed
import gzip
from datetime import datetime # Used to format datetime for mongodb
import time # Limit the number of requests
import pickle # For moving data to a file to be manipulated later

# Based on: http://stackoverflow.com/questions/7894384/
def get_adb_id(adb_link):
    """
    Parses adb_link to get the anidb id at the end
    :param adb_link: the link to the given anime's anidb page
    :return: returns the anidb id for the page
    """
    url = urlparse(adb_link)
    path = url.path
    split_path = os.path.split(path)
    temp_id = split_path[1]
    return temp_id[1:]

# Based on: https://gist.github.com/Manouchehri/0ce55d239fb07c41c92f
def get_adb_data(adb_id):
    """
    Uses the anidb id to get the xml data
    :param adb_id: the anidb id for the anime
    :return: returns the xml data associated with given id
    """
    time.sleep(3)
    url = 'http://api.anidb.net:9001/httpapi?request=anime&client=seasonaljpop&clientver=1&protover=1&aid=' + adb_id
    header = {'Accept-Encoding' : 'gzip'}
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    data = gzip.decompress(response.read())
    return data

def get_adb_airdate(data):
    """
    Uses the given data and searches for the startdata
    :param data: the xml data that will be parsed
    :return: the unformatted starting airdate
    """
    soup = BeautifulSoup(data, 'html.parser')
    date = soup.startdate.contents[0]
    return date

# Date given in string form
# Based on: http://stackoverflow.com/questions/23581128/
def formatted_date(date):
    """
    Processes the date in the form of a string
    :param date: the date represented as a string
    :return: the date as a datetime object
    """
    for fmt in ('%Y', '%Y-%m', '%Y-%m-%d'):
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    raise ValueError('Date does not match formats expected')

def get_vgmdb_music(anime_data):
    """
    Uses the anime data to make a request to vgmdb
    to find music information and pass the appropriate json
    data to get_music()
    http://stackoverflow.com/questions/32795460/loading-json-object-in-python-using-urllib-request-and-json-modules
    :param anime_data: the anime data object which holds title information
    :return: the list of products for this anime
    """
    import urllib.request
    import urllib.parse
    import json
    product_list = []
    time.sleep(2)
    title_jp = anime_data.title_jp
    search_url = 'http://vgmdb.info/search/' + urllib.parse.quote(title_jp) + '?format=json'
    print ('HANDLING', search_url)
    search_request = urllib.request.Request(search_url)
    search_page = urllib.request.urlopen(search_request)
    search_data = search_page.read()
    encoding = search_page.info().get_content_charset('utf-8')
    # Error check json?
    search_json = json.loads(search_data.decode(encoding))
    search_product_link = None
    try:
        # Assumes that the product[0] is good
        search_product_link = search_json['results']['products'][0]['link']
    except IndexError:
        # Return none? NO PRODUCT ;-;
        print ('GetVgmdbWarning: There was no product found for:', title_jp)
        return search_json['results']['albums']
        return product_list
    # Now get product json, assuming there is always a product url
    time.sleep(2)
    product_url = 'http://vgmdb.info/' + search_product_link + '?format=json'
    product_request = urllib.request.Request(product_url)
    product_page = urllib.request.urlopen(product_request)
    product_data = product_page.read()
    product_json = json.loads(product_data.decode(encoding))
    product_list = product_json['albums']
    return product_list

def process_vgmdb_music(anime_data, music_list):
    import anime
    from anime import MusicLink
    processed_list = []
    for music in music_list:
        product_list_found = True
        music_data = None
        # Check date first
        unformatted_date = None
        try:
            unformatted_date = music['date']
        except KeyError:
            # Means a product_list was not found
            print ('ProcessVgmdbWarning: No product_list found, using release_date comparison')
            product_list_found = False
            try:
                unformatted_date = music['release_date']
            except KeyError:
                # No release_date was found so skip this
                print ('ProcessVgmdbWarning: No release_date found, skipping')
                continue
        release_date = formatted_date(unformatted_date)
        if (product_list_found or ((not product_list_found) and (anime_data.airing_date != None) and (anime_data.airing_date <= release_date))):
            # Ensure that at least one value is in the title field
            for title in ['en', 'ja-latn', 'ja']:
                try:
                    music_data = anime.Music(music['titles'][title])
                except KeyError:
                    pass
            # Get other titles
            try:
                music_data.title_en = music['titles']['en']
                music_data.title_rom = music['titles']['ja-latn']
            except KeyError:
                pass
            # Get catalog
            music_data.catalog = music['catalog']
            # Get date
            try:
                music_data.release_date = formatted_date(music['date'])
            except KeyError:
                print ('ProcessVgmdbWarning: Found a song with greater date')
                music_data.release_date = formatted_date(music['release_date'])
                pass
            # Get link
            music_data.links[MusicLink.vgmdb] = 'http://vgmdb.net/' + music['link']
            # Get classifications?
            """
            {
                "classifications": [
                    "Vocal",
                    "OP/ED/Insert"
                ]
            """
            # Add to processed_list
            processed_list.append(music_data)
    return processed_list

#def get_cdjapan_music(anime_data):

def pickle_anime(data):
    """
    Uses the data in the form of a list of anime objects
    and makes it into a pickle file
    :param data: the anime list
    """
    pickle.dump(data, open("save_anime.p", "wb"))

def main():
    import anime
    from anime import AnimeLink
    # Consider not hardcoding the file from the local directory
    soup = BeautifulSoup(open('anime.html'), 'html.parser')
    title_tag_list = soup.find_all('h3')
    anime_list = []
    for title_tag in title_tag_list:
        # Entire tag
        # print(line)
        # Just the contents of the tag
        # print(line.contents)

        # from http://stackoverflow.com/questions/2612548/
        # Get names
        anime_data = anime.Anime(title_tag)
        anime_data.add_titles(title_tag)

        # Get links
        # Need to make tests for when these classes don't exist
        anime_data.add_links(title_tag)

        # Get airdate
        # Process link for ID
        adb_id = get_adb_id(anime_data.links[AnimeLink.adb])
        airdate = None
        # Look up ID on anidb if it exists
        if (adb_id != ''):
            data = get_adb_data(adb_id) # 1970-01-01 is none, incomplete will not have all info
            unformatted_airdate = get_adb_airdate(data)
            # Process date string
            if (unformatted_airdate != '1970-01-01'):
                airdate = formatted_date(unformatted_airdate)
        # Add airdate to anime object
        anime_data.airing_date = airdate

        # Find music on vgmdb
        # Current implementation assumes that a product can be found
        raw_music_list = get_vgmdb_music(anime_data)
        # Process list and add it to the anime_data
        music_list = []
        if (raw_music_list != None):
            music_list = process_vgmdb_music(anime_data, raw_music_list)

        # If music_list is empty, try alternatives
        if (len(music_list) == 0):
            # Need to handle second season stuff
            # Try English instead
            # Search CDJapan

        anime_data.music_list = music_list
        # Add to music database

        # Add to anime list
        anime_list.append(anime_data)
        # break
    # Export to pickle file
    pickle_anime(anime_list)

if __name__ == '__main__':
    main()
