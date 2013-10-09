import unittest
from speakers_scraper import Speakers
import test_util
import timeit

class TestSpeakersScraper(unittest.TestCase):

    def test_get_speakers(self):
        speakers_generator = Speakers(test_util.get_HTML).get_speakers_for_letter('E')
        # First value returned is number of speakers, for progress.
        self.assertTrue(timeit.itertools.islice(speakers_generator, 1).next() > 0)
        e_speakers = list(speakers_generator)
        self.assertTrue(len(e_speakers) > 0)
        self.assertLessEqual(28, len(e_speakers))
        sample_speaker = [s for s in e_speakers if s[0] == 'Kenichi Ebina'][0]
        self.assertEqual('http://www.ted.com/speakers/kenichi_ebina.html', sample_speaker[1])
        self.assertEqual('http://images.ted.com/images/ted/16732_132x99.jpg', sample_speaker[2])

    def test_get_speakers_performance(self):
        scraper = Speakers(test_util.CachedHTMLProvider().get_HTML)
        # Run once to cache.
        speakers = list(scraper.get_speakers_for_letter('B'))
        print "%s speakers found" % (len(speakers))

        def test():
            self.assertEqual(len(speakers), len(list(scraper.get_speakers_for_letter('B'))))

        t = timeit.Timer(test)
        repeats = 2
        time = t.timeit(repeats) / repeats
        print "Getting speakers list took %s seconds per run" % (time)
        self.assertGreater(1, time)

    def test_get_talks_for_speaker(self):
        talks = list(Speakers(test_util.get_HTML).get_talks_for_speaker("http://www.ted.com/speakers/kenichi_ebina.html"))
        print "%s talks for speaker found" % (len(talks))
        self.assertLessEqual(0, len(talks))
        self.assertLessEqual(1, len(talks))

        talk = talks[0]
        self.assertEqual("Kenichi Ebina: My magic moves", talk[0])
        self.assertEqual('http://www.ted.com/talks/kenichi_ebina_s_magic_moves.html', talk[1])
        self.assertEqual('http://images.ted.com/images/ted/16705_113x85.jpg', talk[2])
