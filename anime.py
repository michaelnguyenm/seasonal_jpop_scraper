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
