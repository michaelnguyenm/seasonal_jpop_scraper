import unittest
import anime

class AnimeTests(unittest.TestCase):

    def test_title_only(self):
        a = anime.Anime('Bleach')
        self.assertEqual(a.title_jp, 'Bleach')
        self.assertEqual(a.title_en, None)
        self.assertEqual(a.title_rom, None)
        self.assertEqual(len(a.title_other), 0)
        self.assertEqual(a.title_date, None)
        self.assertEqual(len(a.music_list), 0)

class MusicTests(unittest.TestCase):

    def test_title_only(self):
        m = anime.Music('COLORS')
        self.assertEqual(m.title_jp, 'COLORS')

if __name__ == '__main__':
    unittest.main()
