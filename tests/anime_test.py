import unittest
from seasonal_jpop_scraper import anime

class AnimeTests(unittest.TestCase):

    def test_title_only(self):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup('<h3 data-japanese="Bleach"></h3>', 'html.parser')
        tag = soup.h3
        a = anime.Anime(tag)
        self.assertEqual(a.title_jp, 'Bleach')
        self.assertEqual(a.title_en, None)
        self.assertEqual(a.title_rom, None)
        self.assertEqual(len(a.title_other), 0)
        self.assertEqual(a.airing_date, None)
        self.assertEqual(len(a.music_list), 0)
        self.assertEqual(len(a.links), 3)

    def test_add_titles(self):
        self.assertTrue(True)

    def test_add_links(self):
        self.assertTrue(True)

class MusicTests(unittest.TestCase):

    def test_title_only(self):
        m = anime.Music('COLORS')
        self.assertEqual(m.title_jp, 'COLORS')
        self.assertEqual(m.title_en, None)
        self.assertEqual(m.title_rom, None)
        self.assertEqual(m.catalog, None)
        self.assertEqual(len(m.artist), 0)
        self.assertEqual(m.release_date, None)
        self.assertEqual(len(m.links), 2)

class AnimeLinkTests(unittest.TestCase):

    def test_enums(self):
        self.assertTrue(True)

class MusicLinkTests(unittest.TestCase):

    def test_enums(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
