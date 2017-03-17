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
def formatted_airdate(date):
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
                airdate = formatted_airdate(unformatted_airdate)
        # Add airdate to anime object
        anime_data.airing_date = airdate
        # Find music
        # Add to music database
        # Add to anime list
        anime_list.append(anime_data)
        break
    # Export to pickle file
    pickle_anime(anime_list)

if __name__ == '__main__':
    main()
