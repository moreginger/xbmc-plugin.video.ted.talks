import requests
import talk_scraper
import test_util
import timeit
import unittest


class TestTalkScraper(unittest.TestCase):

    def test_get_2017(self):
        self.assert_talk_details(
            'https://www.ted.com/talks/dan_bricklin_meet_the_inventor_of_the_electronic_spreadsheet',
            u'https://hls.ted.com/talks/2664.m3u8',
            u'Meet the inventor of the electronic spreadsheet',
            u'Dan Bricklin')

    def test_get_2011(self):
        self.assert_talk_details(
            'http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html',
            u'https://hls.ted.com/talks/1338.m3u8',
            u'Know thyself, with a brain scanner',
            u'Ariel Garten')

    def test_get_2003(self):
        self.assert_talk_details(
            'http://www.ted.com/talks/tom_shannon_s_magnetic_sculpture.html',
            u'https://hls.ted.com/talks/534.m3u8',
            u'Anti-gravity sculpture',
            u'Tom Shannon')

    def test_get_youtube(self):
        # This talk was previously only available from YouTube.
        self.assert_talk_details(
            'http://www.ted.com/talks/seth_godin_this_is_broken_1.html',
            u'https://hls.ted.com/talks/953.m3u8',
            u'This is broken',
            u'Seth Godin')

    def assert_talk_details(self, talk_url, expected_video_url, expected_title, expected_speaker):
        video_url, title, speaker, plot, talk_json = talk_scraper.get(
            test_util.get_HTML(talk_url))

        self.assertEqual(
            [expected_video_url, expected_title, expected_speaker],
            [video_url, title, speaker])

        self.assertEqual(200, requests.head(video_url, allow_redirects=True).status_code)
        self.assertTrue(plot)
        self.assertTrue(talk_json)  # Not None or empty

    def test_performance(self):
        html = test_util.get_HTML('http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html')

        t = timeit.Timer(lambda: talk_scraper.get(html))
        repeats = 10
        time = t.timeit(repeats)

        print 'Extracting talk details took %s seconds per run' % (time / repeats)
        self.assertGreater(4, time)
