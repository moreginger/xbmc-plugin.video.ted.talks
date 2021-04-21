import timeit
import unittest

import mock
import requests

from . import talk_scraper
from .test_util import skip_ted_rate_limited, CachedHTMLProvider, EXCLUDE_RATE_LIMITED


class TestTalkScraper(unittest.TestCase):

    def test_get_ted_video(self):
        # pre-2017 talk had different page format at some point. Unsure if that still holds?
        self.assert_talk_details(
            "https://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html",
            "https://hls.ted.com/project_masters/1580/manifest.m3u8?intro_master_id=2346",
            "Know thyself, with a brain scanner",
            "Ariel Garten",
            True,
            True
        )

        # post-2017 talk
        self.assert_talk_details(
            "https://www.ted.com/talks/dan_bricklin_meet_the_inventor_of_the_electronic_spreadsheet",
            "https://hls.ted.com/project_masters/2740/manifest.m3u8?intro_master_id=2346",
            "Meet the inventor of the electronic spreadsheet",
            "Dan Bricklin",
            True,
            True
        )

        # Example of a YouTube link. Not currently working.
        # Correct URL might be something like: plugin://plugin.video.youtube/?action=play_video&videoid=aNDiHSHYI_c
        self.assert_talk_details(
            "https://www.ted.com/talks/seth_godin_this_is_broken_1.html",
            None,
            "This is broken",
            "Seth Godin",
            True,
            True
        )

    def assert_talk_details(self, talk_url, expected_video_url, expected_title, expected_speaker, expect_plot, expect_json):
        logger = mock.MagicMock()
        url, title, speaker, plot, talk_json = talk_scraper.get_talk(CachedHTMLProvider().get_HTML(talk_url), logger)
        self.assertEqual(expected_video_url, url)
        self.assertEqual(expected_title, title)
        self.assertEqual(expected_speaker, speaker)

        if expect_plot:
            self.assertTrue(plot)  # Not None or empty
        else:
            self.assertIsNone(plot)

        if expect_json:
            self.assertTrue(talk_json)  # Not None or empty
        else:
            self.assertIsNone(talk_json)

    def test_performance(self):
        html = CachedHTMLProvider().get_HTML("https://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html")
        logger = mock.MagicMock()

        def test():
            talk_scraper.get_talk(html, logger)

        t = timeit.Timer(test)
        repeats = 10
        time = t.timeit(repeats)
        print(("Extracting talk details took %s seconds per run" % (time / repeats)))
        self.assertGreater(4, time)

