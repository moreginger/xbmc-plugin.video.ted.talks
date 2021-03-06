from future.standard_library import install_aliases
install_aliases()

import unittest
import urllib.request, urllib.error, urllib.parse

from mock import MagicMock

from .model.test_util import CachedHTMLProvider
from . import ted_talks_scraper


class TestTedTalks(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock()
        self.ted_talks = ted_talks_scraper.TedTalks(CachedHTMLProvider().get_HTML, self.logger)

    def test_smoke(self):
        self.ted_talks.getVideoDetails("http://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html", "320kbps")
