import unittest
import anime

class AnimeTests(unittest.TestCase):

    def test_title(self):
        a = anime.Anime('Bleach')
        self.assertEqual(a.title_jp, 'Bleach')

class MusicTests(unittest.TestCase):

    def test_title(self):
        m = anime.Music('COLORS')
        self.assertEqual(m.title_jp, 'COLORS')

if __name__ == '__main__':
    unittest.main()
