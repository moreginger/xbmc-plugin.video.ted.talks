"""
Grab new talks from RSS feed. Yes we can just add an rss: source in XBMC,
but this allows us a little more power to tweak things how we want them,
so keep it for now.
"""

import time
import urllib.request, urllib.error, urllib.parse


try:
    from elementtree.ElementTree import fromstring
except ImportError:
    from xml.etree.ElementTree import fromstring

def get_document(url):
    """
    Return document at given URL.
    """
    usock = urllib.request.urlopen(url)
    try:
        return usock.read()
    finally:
        usock.close()


class NewTalksRss(object):
    """
    Fetches new talks from RSS stream.
    """

    def __init__(self, logger):
        self.logger = logger

    def get_talk_details(self, item):
        """
        Return the details from an RSS <item> tag soup.
        """
        # TODO: Upgrade link to user's bitrate, looks like can synthesize
        # URL of form https://download.ted.com/talks/{lastPathSegment.mp4}

        # get date as XBMC wants it
        pub_date = item.find('./pubDate').text[:-6]  # strptime can't handle timezone info.
        try:
            date = time.strptime(pub_date, "%a, %d %b %Y %H:%M:%S")
        except ValueError as e:
            self.logger("Could not parse date '%s': %s" % (pub_date, e))
            date = time.localtime()

        # convert H:M:S duration to seconds
        duration = item.find('./{http://www.itunes.com/dtds/podcast-1.0.dtd}duration').text
        duration = [0, 0] + duration.split(':')
        duration = (int(duration[-3])*60 + int(duration[-2])*60) + int(duration[-1])

        return {
            'title': item.find('./{http://www.itunes.com/dtds/podcast-1.0.dtd}subtitle').text.strip(),
            'cast': [item.find('./{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text],
            'thumb': item.find('./{http://search.yahoo.com/mrss/}thumbnail').get('url'),
            'plot': item.find('./{http://www.itunes.com/dtds/podcast-1.0.dtd}summary').text,
            'duration': duration,
            'date': time.strftime("%d.%m.%Y", date),
            #'aired': time.strftime("%Y-%m-%d", date),
            'dateadded': time.strftime("%Y-%m-%d %H:%M:%S", date),
            'url': item.find('./link').text,
            'media': item.find('./{http://search.yahoo.com/mrss/}content').get('url'),
            'mediatype': 'video'
        }

    def get_new_talks(self, feed=None):
        if not feed:
            feed = 'http://feeds.feedburner.com/tedtalks_video'
        """
        Returns talks as dicts:
        {title:, author:, thumb:, date:, duration:, link: ...}.
        """
        talks_by_title = {}
        rss = get_document(feed)
        for item in fromstring(rss).findall('channel/item'):
            talk = self.get_talk_details(item)
            talks_by_title[talk['title']] = talk

        return iter(talks_by_title.values())
