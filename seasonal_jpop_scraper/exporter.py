from anime import AnimeLink
from anime import MusicLink
from anime import Anime
from anime import Music
from pymongo import MongoClient
import datetime as dt

def parse_args(args):
    """
    Parses the args for use in the script
    :param args: The arguments in a list
    :return: returns arguments that have been parse
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Exports the pickle file to mongodb'
    )
    parser.add_argument('-m', action='store',
                        dest='addr',
                        default='localhost:27017',
                        help='A mongodb address')
    parser.add_argument('-p', action='store',
                        dest='file_name',
                        default='save_anime.p',
                        help='An input pickle file')
    return parser.parse_args(args)

def unpickle_anime(file_name):
    """
    Takes in a file name to load a pickle file as a list
    :param file_name: The file name of the pickle file
    :return: returns the list in this pickle file
    """
    import pickle
    anime_list = pickle.load(open(file_name, "rb"))
    total_music = 0
    for anime_obj in anime_list:
        print('ANIME:', anime_obj.title_jp)
        for music_obj in anime_obj.music_list:
            total_music += 1
            print('MUSIC:', music_obj.title_jp)
            print('LINK:', music_obj.links[MusicLink.vgmdb])
    print('There is/are', len(anime_list), 'element(s) in the unpickled list.')
    print('There is/are', total_music, 'music in the unpickled list.')
    return anime_list

# http://stackoverflow.com/questions/765797/python-timedelta-in-years
def years_ago(years, from_date=None):
    if from_date is None:
        from_date = dt.now()
    try:
        return from_date.replace(year=from_date.year - years)
    except ValueError:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28, year=from_date.year-years)

def num_years(begin, end=None):
    if end is None:
        end = dt.now()
    num_years = int((end - begin).days / 365.2425)
    if begin > years_ago(num_years, end):
        return num_years - 1
    else:
        return num_years

def date_to_season(date):
    """
    result = 0
    # Need to determine years ago from 2016-12-01
    year_diff = num_years(dt.datetime(2016, 12, 1), date)
    result += year_diff * 4
    """
    # Need to calculate season
    if(dt.datetime(date.year - 1, 12, 1) <= date and dt.datetime(date.year, 3, 1) > date):
        return '0'
    elif(dt.datetime(date.year, 3, 1) <= date and dt.datetime(date.year, 6, 1) > date):
        return '1'
    elif(dt.datetime(date.year, 6, 1) <= date and dt.datetime(date.year, 9, 1) > date):
        return '2'
    else:
        return '3'

def main():
    import sys

    # Parse arguments
    args = parse_args(sys.argv[1:])

    # Check if mongodb
    # url_check(args.addr)
    # mongodb://192.168.99.100:32768/

    anime_list = unpickle_anime(args.file_name)

    # Connect to mongodb
    client = MongoClient(args.addr)
    seasonal_jpop = client.seasonal_jpop

    # Iterate through anime_list
    music_total_list = 0
    music_total_upserts = 0
    for anime_obj in anime_list:
        # Process Music in anime
        music_list = []
        for music_obj in anime_obj.music_list:
            music_entry =   {
                                "title_jp": music_obj.title_jp,
                                "title_en": music_obj.title_en,
                                "title_rom": music_obj.title_rom,
                                "catalog": music_obj.catalog,
                                "artist": music_obj.artist,
                                "release_date": music_obj.release_date,
                                "links": {
                                    "amazon": music_obj.links[MusicLink.amazon],
                                    "vgmdb": music_obj.links[MusicLink.vgmdb]
                                }
                            }
            music_result = seasonal_jpop.music.update_one({"title_jp": music_obj.title_jp}, {'$set': music_entry}, upsert = True)
            # Causes problems with ensuring that all music gets added to the music list for a given anime
            # Not everything has an upserted_id
            if(music_result.upserted_id != None):
                music_list.append(music_result.upserted_id)
                music_total_upserts += 1
            '''
            else:
                music_result = seasonal_jpop.music.find_one({"title_jp": music_obj.title_jp})['_id']
                music_list.append(music_result)
            '''
        music_total_list += len(anime_obj.music_list)
        # Process Anime
        anime_entry =   {
                            "title_jp": anime_obj.title_jp,
                            "title_en": anime_obj.title_en,
                            "title_rom": anime_obj.title_rom,
                            "title_other": anime_obj.title_other,
                            "airing_date": anime_obj.airing_date,
                            "music_list": music_list,
                            "links": {
                                "mal": anime_obj.links[AnimeLink.mal],
                                "adb": anime_obj.links[AnimeLink.adb],
                                "kitsu": anime_obj.links[AnimeLink.kitsu]
                            }
                        }
        anime_result = seasonal_jpop.anime.update_one({"title_jp": anime_obj.title_jp}, {'$set': anime_entry}, upsert = True)
        # print(anime_result.inserted_id)
        # Insert anime into correct year/seasonal_jpop
        # Check if None
        anime_date = anime_obj.airing_date
        anime_season = date_to_season(anime_date)
        if(anime_result.upserted_id != None):
            season_result = seasonal_jpop.seasons.update_one({"year": anime_date.year}, {'$push': {anime_season: anime_result.upserted_id}}, upsert = True)

    '''
    import pprint
    for entry in seasonal_jpop.anime.find():
        pprint.pprint(entry)
    '''
    print('There are', music_total_upserts, '/', music_total_list, 'music objects in anime objects')

if __name__ == '__main__':
    main()

"""
Season
result = seasonal_jpop.seasons.update_one({'year': '2017'},{'$push': {'0': 'test'}}, upsert=True)
{
    1: [List of anime],
    2: [...],
    3: [...],
    ...
}

Artist
{
    _id: index,
    "name": music_obj.artist[...],
    "music_list": [List of music objects]
}
"""
