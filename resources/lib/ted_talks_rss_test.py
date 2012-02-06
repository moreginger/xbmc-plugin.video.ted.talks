import unittest
import ted_talks_rss
from datetime import datetime
from BeautifulSoup import BeautifulStoneSoup

class TestGetTalkDetails(unittest.TestCase):
    
    def test_minimal(self):
        item = """
<item>
  <itunes:author>Dovahkiin</itunes:author>
  <itunes:subtitle>fus ro dah</itunes:subtitle>
  <pubDate>Sat, 04 Feb 2012 08:14:00 +0000</pubDate>
  <media:thumbnail url="invalid://nowhere/nothing.jpg" width="42" height="42" />
  <enclosure url="invalid://nowhere/nothing.mp4" length="42" type="video/mp4" />
</item>
"""
        details = ted_talks_rss.getTalkDetails(BeautifulStoneSoup(item).item)
        expectedDetails = {
            'author':u'Dovahkiin',
            'date':'04.02.2012',
            'link':u'invalid://nowhere/nothing.mp4',
            'thumb':u'invalid://nowhere/nothing.jpg',
            'title':u'fus ro dah'
        }
        self.assertEqual(expectedDetails, details)
        
    def test_broken_date(self):
        item = """
<item>
  <itunes:author>Dovahkiin</itunes:author>
  <itunes:subtitle>fus ro dah</itunes:subtitle>
  <pubDate>Sat, 04 02 2012 08:14:00</pubDate>
  <media:thumbnail url="invalid://nowhere/nothing.jpg" width="42" height="42" />
  <enclosure url="invalid://nowhere/nothing.mp4" length="42" type="video/mp4" />
</item>
"""
        details = ted_talks_rss.getTalkDetails(BeautifulStoneSoup(item).item)
        expectedDetails = {
            'author':u'Dovahkiin',
            'date':datetime.strftime(datetime.now(), "%d.%m.%Y"), # Using now() kind of stinks so don't run at midnight!
            'link':u'invalid://nowhere/nothing.mp4',
            'thumb':u'invalid://nowhere/nothing.jpg',
            'title':u'fus ro dah'
        }
        self.assertEqual(expectedDetails, details)


class TestNewTalksRss(unittest.TestCase):
    
    def setUp(self):
        self.talks = ted_talks_rss.NewTalksRss(lambda x: x)

    def test_smoke(self):
        talks = list(self.talks.getNewTalks())
        # Need to assert more, but if it didn't explode that is a start.
        print talks[0]

