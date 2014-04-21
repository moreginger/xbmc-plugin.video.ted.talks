import unittest
from topics_scraper import Topics
import test_util
import timeit


class TestTopicsScraper(unittest.TestCase):

    def test_get_topics(self):
        e_topics = list(Topics(test_util.get_HTML).get_topics())
        self.assertTrue(len(e_topics) > 0)
        sample_topic = [t for t in e_topics if t[0] == 'Activism'][0]
        self.assertEqual('http://www.ted.com/topics/activism', sample_topic[1])

    def test_get_topics_performance(self):
        scraper = Topics(test_util.CachedHTMLProvider().get_HTML)
        # Run once to cache.
        topics = list(scraper.get_topics())
        print "%s topics found" % (len(topics))

        def test():
            self.assertEqual(len(topics), len(list(scraper.get_topics())))

        t = timeit.Timer(test)
        repeats = 2
        time = t.timeit(repeats) / repeats
        print "Getting topics list took %s seconds per run" % (time)
        self.assertGreater(1, time)

    def test_get_talks(self):
        e_talks = list(Topics(test_util.get_HTML).get_talks('http://www.ted.com/topics/activism'))
        self.assertLess(0, len(e_talks))
        self.assertLessEqual(55, len(e_talks))
        sample_talk = [t for t in e_talks if t[0] == "Jennifer Pahlka: Coding a better government"][0]
        self.assertEqual('http://www.ted.com/talks/jennifer_pahlka_coding_a_better_government', sample_talk[1])
        self.assertEqual('http://images.ted.com/images/ted/8a3803576b960b90b3f55b6c0edab9eb8eb2f0fa_132x99.jpg', sample_talk[2])

    def test_get_talks_performance(self):
        scraper = Topics(test_util.CachedHTMLProvider().get_HTML)
        # Run once to cache.
        talks = list(scraper.get_talks('http://www.ted.com/topics/activism'))
        print "%s talks for topic found" % (len(talks))

        def test():
            self.assertEqual(len(talks), len(list(scraper.get_talks('http://www.ted.com/topics/activism'))))

        t = timeit.Timer(test)
        repeats = 2
        time = t.timeit(repeats) / repeats
        print "Getting talks for topic took %s seconds per run" % (time)
        self.assertGreater(1, time)
