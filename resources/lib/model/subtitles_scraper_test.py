import sys
import time
import unittest

from mock import MagicMock

from . import talk_scraper
from .subtitles_scraper import Subtitles
from .test_util import skip_ted_rate_limited, CachedHTMLProvider

class TestSubtitlesScraper(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock()
        self.fetcher = CachedHTMLProvider()
        self.sut = Subtitles(self.fetcher, self.logger)
    
    def tearDown(self):
        self.logger.assert_not_called()

    def test_format_time(self):
        self.assertEqual('00:00:00,000', self.sut.__format_time__(0))
        self.assertEqual('03:25:45,678', self.sut.__format_time__(12345678))

    def test_format_subtitles(self):
        subtitles = [{'content': 'Hello', 'start': 500, 'duration': 2500}, {'content': 'World', 'start': 3000, 'duration': 2500}]
        formatted_subs = self.sut.__format_subtitles__(subtitles, 666)
        self.assertEqual('''1
00:00:01,166 --> 00:00:03,666
Hello

2
00:00:03,666 --> 00:00:06,166
World

''', formatted_subs)

    def test_get_languages_and_get_subtitles_for_talk(self):
        talk_json = self.__get_talk_json__('http://www.ted.com/talks/richard_wilkinson.html')
        expected = set(['ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en', 'es', 'eu', 'fa', 'fr', 'gl', 'he', 'hr', 'hu', 'hy', 'id', 'it', 'ja', 'ka', 'ko', 'mk', 'nb', 'nl', 'pl', 'pt', 'pt-br', 'ro', 'ru', 'sk', 'sq', 'sr', 'sv', 'th', 'tr', 'uk', 'vi', 'zh-cn', 'zh-tw'])
        result = set(self.sut.__get_languages__(talk_json))
        self.assertEqual(expected, result, msg="New translations are likely to appear; please update the test if so :)\n%s" % (sorted(result)))

        subs = self.sut.get_subtitles_for_talk(talk_json, ['banana', 'fr', 'en'])
        self.assertIn('''1
00:00:02,504 --> 00:00:05,504
Vous savez tous que ce que je vais dire est vrai.

2''', subs)

    def __get_talk_json__(self, url):
        html = self.fetcher.get_HTML(url)
        foo, fi, fo, fum, talk_json = talk_scraper.get_talk(html, self.logger)
        return talk_json
