import unittest
import scraper

class ScraperTests(unittest.TestCase):

    def test_get_adb_id_1(self):
        adb_id = scraper.get_adb_id('http://anidb.net/a12506')
        self.assertEqual(adb_id, '12506')

    def test_get_adb_id_2(self):
        adb_id = scraper.get_adb_id('http://anidb.net/a1')
        self.assertEqual(adb_id, '1')

    def test_get_adb_id_empty(self):
        adb_id = scraper.get_adb_id('')
        self.assertEqual(adb_id,'')

if __name__ == '__main__':
    unittest.main()
