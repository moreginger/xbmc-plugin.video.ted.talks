import unittest
import urllib2

import ted_talks_scraper
import model.test_util as test_util


class TestTedTalks(unittest.TestCase):

    def setUp(self):
        self.ted_talks = ted_talks_scraper.TedTalks(test_util.get_HTML, None)

    def test_smoke(self):
        self.ted_talks.getVideoDetails("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html", "320kbps")
