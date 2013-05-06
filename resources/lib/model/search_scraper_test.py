import unittest
from search_scraper import Search
import test_util
import timeit

class TestSearchScraper(unittest.TestCase):

    def test_get_talks_for_search_smoke(self):
        scraper = Search(test_util.get_HTML)
        talks_generator = scraper.get_talks_for_search('nuclear', 1)
        remaining_talks = timeit.itertools.islice(talks_generator, 1).next()
        self.assertGreater(0, remaining_talks)
        
        talks = list(talks_generator)
        # One page at a time
        self.assertEqual(10, len(talks))
        # Actually no quarantee this talk is in top ten results. It is today.
        sample_talk = [s for s in talks if s[0] == 'Taylor Wilson: My radical plan for small nuclear fission reactors'][0]
        self.assertEqual('http://www.ted.com/talks/george_dyson_on_project_orion.html', sample_talk[1])
        self.assertEqual('http://images.ted.com/images/ted/30129_74x56.jpg', sample_talk[2])
        
        last_page = 1 + (remaining_talks / 10)
        talks_generator = scraper.get_talks_for_search('nuclear', last_page)
        remaining_talks = timeit.itertools.islice(talks_generator, 1).next()
        self.assertEqual(0, remaining_talks)
        self.assertLess(0, len(talks))
        