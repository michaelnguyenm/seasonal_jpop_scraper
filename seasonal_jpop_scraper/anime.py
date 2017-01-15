from enum import Enum

"""
This module contains all the classes necessary to have information on a given
anime and its associated artists and music
"""

class Music:
    """
    Stores the information about a given music object
    Requires at least a title in Japanese
    """

    def __init__(self, title_jp):
        """
        Constructs a new 'Music' object
        :param title_jp: The title of the music in Japanese
        :return: returns nothing
        """
        self.title_jp = title_jp
        self.title_en = None
        self.title_rom = None
        self.artist = []
        self.release_date = None
        self.music_links = []

class AnimeLink(Enum):
    mal = 1;
    adb = 2;
    kitsu = 3;

class Anime:
    """
    Stores the information about this anime
    Requires at least a title in Japanese
    """

    def __init__(self, title_jp):
        """
        Constructs a new 'Anime' object
        :param title_jp: The title of the anime in Japanese
        :return: returns nothing
        """
        self.title_jp = title_jp
        self.title_en = None
        self.title_rom = None
        self.title_other = []
        self.airing_date = None
        self.music_list = []
        self.anime_links = {AnimeLink.mal:'',
                            AnimeLink.adb:'',
                            AnimeLink.kitsu: ''}

    def add_titles(self, tag):
        """
        Parses the given tag and adds the extra titles
        :param tag: the tag object with the extra titles
        """
        self.title_rom = tag.get('data-romaji')
        self.title_en = tag.get('data-english')
        self.title_other = tag.get('data-alternate').split(',')

    def add_links(self, tag):
        """
        Parses the given tag and adds the links
        :param tag: the tag object with the links
        """
        mal_tag = tag.find_next('a', {'class':'mal-icon'})
        mal_link = '' if mal_tag == None else mal_tag.get('href')
        self.anime_links[AnimeLink.mal] = mal_link
        adb_tag = tag.find_next('a', {'class':'anidb-icon'})
        adb_link = '' if adb_tag == None else adb_tag.get('href')
        self.anime_links[AnimeLink.adb] = adb_link
        kitsu_tag = tag.find_next('a', {'class':'kitsu-icon'})
        kitsu_link = '' if kitsu_tag == None else kitsu_tag.get('href')
        self.anime_links[AnimeLink.kitsu] = kitsu_link
