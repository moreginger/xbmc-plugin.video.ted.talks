import unittest
import urllib2
import ted_talks_scraper

class MockFetcher:

    def getHTML(self, url):
        usock = urllib2.urlopen(url)
        try:
            return usock.read()
        finally:
            usock.close()


class TestTedTalks(unittest.TestCase):
    
    def setUp(self):
        self.fetcher = MockFetcher()
        self.tedTalks = ted_talks_scraper.TedTalks(self.fetcher)

    def test_smoke(self):
        self.tedTalks.getVideoDetails("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")
        self.tedTalks.getVideoDetails("http://www.ted.com/talks/bjarke_ingels_hedonistic_sustainability.html")


class TestNewTalks(unittest.TestCase):

    def setUp(self):
        self.fetcher = MockFetcher()
        self.newTalks = ted_talks_scraper.TedTalks.NewTalks(self.fetcher)

    def test_smoke(self):
        self.newTalks.getNewTalks()
