import unittest
from speakers_scraper import Speakers
import urllib2

def get_HTML(url):
    return urllib2.urlopen(url).read()

class TestSpeakersScraper(unittest.TestCase):

    def test_get_speakers(self):
        print list(Speakers(get_HTML).get_speakers_for_letter('E'))
