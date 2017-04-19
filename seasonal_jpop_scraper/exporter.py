import pickle
from anime import AnimeLink
from anime import MusicLink
from anime import Anime
from anime import Music
from pymongo import MongoClient
from datetime import datetime

def unpickle_anime():
    anime_list = pickle.load(open("save_anime.p", "rb"))
    print('There is/are', len(anime_list), 'element(s) in the unpickled list.')
    for anime_obj in anime_list:
        print('ANIME:', anime_obj.title_jp)
        for music_obj in anime_obj.music_list:
            print('MUSIC:', music_obj.title_jp)
    return anime_list

def main():
    anime_list = unpickle_anime()

    connection = "mongodb://192.168.99.100:32768"
    client = MongoClient(connection)
    seasonal_jpop = client.seasonal_jpop
    """
    result = db.restaurants.insert_one(
        {
            "address": {
                "street": "2 Avenue",
                "zipcode": "10075",
                "building": "1480",
                "coord": [-73.9557413, 40.7720266]
            },
            "borough": "Manhattan",
            "cuisine": "Italian",
            "grades": [
                {
                    "date": datetime.strptime("2014-10-01", "%Y-%m-%d"),
                    "grade": "A",
                    "score": 11
                },
                {
                    "date": datetime.strptime("2014-01-16", "%Y-%m-%d"),
                    "grade": "B",
                    "score": 17
                }
            ],
            "name": "Vella",
            "restaurant_id": "41704620"
        }
    )
    """
    for anime_obj in anime_list:
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
            result = seasonal_jpop.music.insert_one(music_entry);
            music_list.append(result.inserted_id)
        result = seasonal_jpop.anime.insert_one(
            {
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
        )
        print(result.inserted_id)

if __name__ == '__main__':
    main()

"""
Season
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
