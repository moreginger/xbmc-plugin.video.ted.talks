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

    def test_get_ted_video(self):
        self.scraper = Talk(get_HTML)
        self.assert_talk_details("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html", "http://download.ted.com/talks/ArielGarten_2011X.mp4", u"Know thyself, with a brain scanner", u"Ariel Garten")

    def test_get_youtube_video(self):
        self.scraper = Talk(get_HTML)
        self.assert_talk_details("http://www.ted.com/talks/bjarke_ingels_hedonistic_sustainability.html", "plugin://plugin.video.youtube/?action=play_video&videoid=ogXT_CI7KRU", u"Hedonistic sustainability", u"Bjarke Ingels")

    def test_get_vimeo_video(self):
        self.scraper = Talk(get_HTML)
        self.assert_talk_details("http://www.ted.com/talks/seth_godin_this_is_broken_1.html", "plugin://plugin.video.vimeo?action=play_video&videoid=4246943", u"This is broken", u"Seth Godin")

    def assert_talk_details(self, talk_url, expected_video_url, expected_title, expected_speaker):
        video_url, title, speaker, plot = self.scraper.get(talk_url)
        self.assertEqual(expected_video_url, video_url)
        self.assertEqual(expected_title, title)
        self.assertEqual(expected_speaker, speaker)
        self.assertTrue(plot)  # Not null or empty.

    def test_performance(self):
        html = get_HTML("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")

        def test():
            timing_run(html);

        t = timeit.Timer(test)
        repeats = 10
        time = t.timeit(repeats)
        print "Extracting talk details took %s seconds per run" % (time / repeats)
        self.assertGreater(4, time)

