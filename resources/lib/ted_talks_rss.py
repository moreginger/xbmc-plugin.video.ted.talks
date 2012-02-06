import urllib2
from datetime import datetime
from BeautifulSoup import SoupStrainer, BeautifulStoneSoup
import plugin

def getDocument(url):
    """
    Return document at given URL.
    """
    usock = urllib2.urlopen(url)
    try:
        return usock.read()
    finally:
        usock.close()

def getTalkDetails(item):
    """
    Return the details from an RSS <item> tag soup.
    """
    title = item.find('itunes:subtitle').string # <title> tag has unecessary padding strings
    author = item.find('itunes:author').string
    # Get date as XBMC wants it
    try:
        date = datetime.strptime(item.pubdate.string[:-6], "%a, %d %b %Y %H:%M:%S")
    except ValueError, e:
        print '[%s] %s Could not parse date: %s' % (plugin.__plugin__, __name__, item.pubdate.string)
        print e
        date = datetime.now()
    date = datetime.strftime(date, "%d.%m.%Y")
        
    pic = item.find('media:thumbnail')['url']
    link = item.enclosure['url']
    return {'title':title, 'author':author, 'thumb':pic, 'date':date, 'link':link}


class NewTalksRss:
    """
    Fetches new talks from RSS stream.
    """
 
    def getNewTalks(self):
        """
        Returns talks as dicts {title:, author:, thumb:, date:, link:}.
        """
        
        rss_url = "http://feeds.feedburner.com/tedtalks_video"
        rss = getDocument(rss_url)
        
        items = SoupStrainer(name='item')
        for item in BeautifulStoneSoup(rss, parseOnlyThese = items):
            yield getTalkDetails(item)
