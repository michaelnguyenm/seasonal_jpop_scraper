import unittest
import anime

class AnimeTests(unittest.TestCase):

    def test_title_only(self):
        a = anime.Anime('Bleach')
        self.assertEqual(a.title_jp, 'Bleach')
        self.assertEqual(a.title_en, None)
        self.assertEqual(a.title_rom, None)
        self.assertEqual(len(a.title_other), 0)
        self.assertEqual(a.airing_date, None)
        self.assertEqual(len(a.music_list), 0)
        self.assertEqual(len(a.anime_links), 0)

class MusicTests(unittest.TestCase):

    def test_title_only(self):
        m = anime.Music('COLORS')
        self.assertEqual(m.title_jp, 'COLORS')
        self.assertEqual(m.title_en, None)
        self.assertEqual(m.title_rom, None)
        self.assertEqual(len(m.artist), 0)
        self.assertEqual(m.release_date, None)
        self.assertEqual(len(m.music_links), 0)

if __name__ == '__main__':
    unittest.main()
