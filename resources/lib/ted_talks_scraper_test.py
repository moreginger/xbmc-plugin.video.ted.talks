import unittest
import urllib2
import ted_talks_scraper

def getHTML(url):
    usock = urllib2.urlopen(url)
    try:
        return usock.read()
    finally:
        usock.close()


class TestTedTalks(unittest.TestCase):
    
    def setUp(self):
        self.tedTalks = ted_talks_scraper.TedTalks(getHTML)

    def test_smoke(self):
        self.tedTalks.getVideoDetails("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")
        self.tedTalks.getVideoDetails("http://www.ted.com/talks/bjarke_ingels_hedonistic_sustainability.html")


class TestNewTalks(unittest.TestCase):

    def setUp(self):
        self.newTalks = ted_talks_scraper.NewTalks(getHTML, lambda code: "%s" % code)

    def test_smoke(self):
        newTalks = list(self.newTalks.getNewTalks())
        nextPage = newTalks[0]
        self.assertTrue(nextPage[0])
        firstTalk = newTalks[1]
        self.assertFalse(firstTalk[0])
