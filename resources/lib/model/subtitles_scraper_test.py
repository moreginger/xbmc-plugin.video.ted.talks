import unittest
import subtitles_scraper
import urllib
from BeautifulSoup import MinimalSoup

class TestSubtitlesScraper(unittest.TestCase):
    
    def test_format_time(self):
        self.assertEqual('00:00:00,000', subtitles_scraper.format_time(0))
        self.assertEqual('03:25:45,678', subtitles_scraper.format_time(12345678))

    def test_get_languages(self):
        soup = MinimalSoup(urllib.urlopen('http://www.ted.com/talks/richard_wilkinson.html').read())
        expected = ['sq', 'ar', 'hy', 'bg', 'ca', 'zh-cn', 'zh-tw', 'hr', 'cs', 'da', 'nl', 'en', 'fr', 'ka', 'de', 'el', 'he', 'hu', 'id', 'it', 'ja', 'ko', 'fa', 'pl', 'pt-br', 'pt', 'ro', 'ru', 'sr', 'sk', 'es', 'th', 'tr', 'uk', 'vi']
        self.assertEqual(expected, subtitles_scraper.get_languages(soup))