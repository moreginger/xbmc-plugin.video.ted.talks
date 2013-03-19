import unittest
import talk_scraper
import urllib2
import timeit


def get_HTML(url):
    return urllib2.urlopen(url).read()


class TestTalkScraper(unittest.TestCase):

    def test_get_ted_video(self):
        self.assert_talk_details("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html", "http://download.ted.com/talks/ArielGarten_2011X.mp4", u"Know thyself, with a brain scanner", u"Ariel Garten")

    def test_get_youtube_video(self):
        self.assert_talk_details("http://www.ted.com/talks/bjarke_ingels_hedonistic_sustainability.html", "plugin://plugin.video.youtube/?action=play_video&videoid=ogXT_CI7KRU", u"Hedonistic sustainability", u"Bjarke Ingels")

    def test_get_vimeo_video(self):
        self.assert_talk_details("http://www.ted.com/talks/seth_godin_this_is_broken_1.html", "plugin://plugin.video.vimeo?action=play_video&videoid=4246943", u"This is broken", u"Seth Godin")

    def assert_talk_details(self, talk_url, expected_video_url, expected_title, expected_speaker):
        video_url, title, speaker, plot = talk_scraper.get(get_HTML(talk_url))
        self.assertEqual(expected_video_url, video_url)
        self.assertEqual(expected_title, title)
        self.assertEqual(expected_speaker, speaker)
        self.assertTrue(plot)  # Not null or empty.

    def test_get_custom_quality_video(self):
        html = get_HTML("http://www.ted.com/talks/edith_widder_how_we_found_the_giant_squid.html")
        # Note not customized. Should be a useful fallback if this code goes haywire.
        self.assert_custom_quality_url(html, 3, "http://download.ted.com/talks/EdithWidder_2013.mp4")

        self.assert_custom_quality_url(html, 1, "http://download.ted.com/talks/EdithWidder_2013-64k.mp4")
        self.assert_custom_quality_url(html, 2, "http://download.ted.com/talks/EdithWidder_2013-180k.mp4")
        self.assert_custom_quality_url(html, 4, "http://download.ted.com/talks/EdithWidder_2013-450k.mp4")
        self.assert_custom_quality_url(html, 5, "http://download.ted.com/talks/EdithWidder_2013-600k.mp4")
        self.assert_custom_quality_url(html, 6, "http://download.ted.com/talks/EdithWidder_2013-950k.mp4")
        self.assert_custom_quality_url(html, 7, "http://download.ted.com/talks/EdithWidder_2013-1500k.mp4")

        # Fall back to standard URL when custom URL 404s
        self.assert_custom_quality_url(html, 42, "http://download.ted.com/talks/EdithWidder_2013.mp4")

        try:
            self.assert_custom_quality_url(html, 8, "will blow up")
            self.fail()
        except KeyError:
            pass

    def assert_custom_quality_url(self, talk_html, video_quality, expected_video_url):
        video_url, title, speaker, plot = talk_scraper.get(talk_html, video_quality)
        self.assertEqual(expected_video_url, video_url)

    def test_performance(self):
        html = get_HTML("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")

        def test():
            talk_scraper.get(html);

        t = timeit.Timer(test)
        repeats = 10
        time = t.timeit(repeats)
        print "Extracting talk details took %s seconds per run" % (time / repeats)
        self.assertGreater(4, time)

