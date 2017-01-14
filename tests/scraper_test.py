import unittest
from seasonal_jpop_scraper import scraper
from datetime import datetime

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

    def test_formatted_airdate(self):
        date = scraper.formatted_airdate('1970-01')
        self.assertEqual(date, datetime(1970, 1, 1))

if __name__ == '__main__':
    unittest.main()
