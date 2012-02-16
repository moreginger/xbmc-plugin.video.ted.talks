import unittest
import arguments

class TestNewTalksRss(unittest.TestCase):
    
    def test_parse_arguments(self):
        self.assertEqual({'mode': 'rn_life_is_rubbish'}, arguments.parse_arguments("?mode=rn_life_is_rubbish"))
        self.assertEqual({'a': '1', 'b': '2'}, arguments.parse_arguments("?a=1&b=2"))