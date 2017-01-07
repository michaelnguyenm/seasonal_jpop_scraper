import unittest
import retriever

class RetrieverTests(unittest.TestCase):

    def test_arg_parsing_both(self):
        test_args = retriever.parse_args(['-u', 'https://livechart.me', '-o', 'a.out'])
        self.assertEqual(test_args.url, 'https://livechart.me')
        self.assertEqual(test_args.file_name, 'a.out')

    def test_arg_parsing_url(self):
        test_args = retriever.parse_args(['-o', 'test.html'])
        self.assertEqual(test_args.url, 'https://www.livechart.me/')
        self.assertEqual(test_args.file_name, 'test.html')

    def test_arg_parsing_file(self):
        test_args = retriever.parse_args(['-u', 'https://google.com'])
        self.assertEqual(test_args.url, 'https://google.com')
        self.assertEqual(test_args.file_name, 'anime.html')

    def test_arg_parsing_none(self):
        test_args = retriever.parse_args([])
        self.assertEqual(test_args.url, 'https://www.livechart.me/')
        self.assertEqual(test_args.file_name, 'anime.html')

    def test_url_checking_all_error(self):
        with self.assertRaises(Exception):
            retriever.url_check('a')

    def test_url_checking_http_missing(self):
        with self.assertRaises(Exception):
            retriever.url_check('livechart.me')

    def test_url_checking_livechart_missing(self):
        with self.assertRaises(Exception):
            retriever.url_check('https://')

    def test_url_checking_no_error(self):
        retriever.url_check('http://livechart.me/')

if __name__ == '__main__':
    unittest.main()
