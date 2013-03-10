import unittest
from talk_scraper import Talk
import urllib2
import timeit


def get_HTML(url):
    return urllib2.urlopen(url).read()

def timing_run(html):
    scraper = Talk(lambda x: html)
    scraper.get(None);


class TestTalkScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Talk(get_HTML)

    def test_smoke(self):
        html = get_HTML("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")

        def test():
            timing_run(html);

        t = timeit.Timer(test)
        self.assertGreater(10, t.timeit(10))

#        self.talk.get("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")
#        self.ted_talks.getVideoDetails("http://www.ted.com/talks/bjarke_ingels_hedonistic_sustainability.html")



