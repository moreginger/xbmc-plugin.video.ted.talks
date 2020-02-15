from __future__ import print_function

import unittest

from . import fetcher

class TestFetch(unittest.TestCase):

    def test_Fetcher(self):
        sut = fetcher.Fetcher(lambda x: print(x))
        sut.getHTML('http://www.google.com/') # Doesn't throw
