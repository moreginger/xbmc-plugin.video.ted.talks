import unittest
from search_scraper import Search
import test_util
import timeit
import math

class TestSearchScraper(unittest.TestCase):

    def test_get_talks_for_search_smoke(self):
        scraper = Search(test_util.get_HTML)
        talks_generator = scraper.get_talks_for_search('nuclear', 1)
        remaining_talks = timeit.itertools.islice(talks_generator, 1).next()

        self.assertLess(100, remaining_talks)  # 925 (!) results at last check, just make sure we have a decent number remaining.

        talks = list(talks_generator)
        talks_per_page = 12.0
        self.assertEqual(talks_per_page, len(talks))
        # Actually no quarantee this talk is in top ten results. It is today.
        sample_talk = [s for s in talks if s[0] == 'Taylor Wilson: My radical plan for small nuclear fission reactors'][0]
        self.assertEqual('http://www.ted.com/talks/taylor_wilson_my_radical_plan_for_small_nuclear_fission_reactors', sample_talk[1])
        self.assertEqual('http://images.ted.com/images/ted/a39d3332aa3d0cabe2e4c20ffb1a3934c012ee8b_240x180.jpg', sample_talk[2])

        last_page = 1 + int(math.ceil(remaining_talks / talks_per_page))
        talks_generator = scraper.get_talks_for_search('nuclear', last_page)
        remaining_talks = timeit.itertools.islice(talks_generator, 1).next()
        self.assertEqual(0, remaining_talks)
        self.assertLess(0, len(talks))
