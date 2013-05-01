import unittest
from speakers_scraper import Speakers
import urllib2
import timeit

def get_HTML(url):
    return urllib2.urlopen(url).read()

class TestSpeakersScraper(unittest.TestCase):

    def test_get_speakers(self):
        speakers_generator = Speakers(get_HTML).get_speakers_for_letter('E')
        # First value returned is number of speakers, for progress.
        self.assertTrue(timeit.itertools.islice(speakers_generator, 1).next() > 0)
        e_speakers = list(speakers_generator)
        self.assertTrue(len(e_speakers) > 0)
        sample_speaker = [s for s in e_speakers if s[0] == 'Kenichi Ebina'][0]
        self.assertEqual('http://www.ted.com/speakers/kenichi_ebina.html', sample_speaker[1])
        self.assertEqual('http://images.ted.com/images/ted/16732_132x99.jpg', sample_speaker[2])

    def test_performance(self):
        cached_html = {}
        def get_HTML_cached(url):
            if url not in cached_html:
                cached_html[url] = get_HTML(url)
            return cached_html[url]

        scraper = Speakers(get_HTML_cached)
        # Run once to cache.
        speakers = list(scraper.get_speakers_for_letter('B'))
        
        def test():
            self.assertEqual(len(speakers), len(list(scraper.get_speakers_for_letter('B'))))

        t = timeit.Timer(test)
        repeats = 2
        time = t.timeit(repeats) / repeats
        print "Getting speakers list took %s seconds per run" % (time)
        self.assertGreater(20, time)
