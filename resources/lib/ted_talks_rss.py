import urllib2
import time
import plugin
try:    
    from elementtree.ElementTree import fromstring
except ImportError:
    from xml.etree.ElementTree import fromstring

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
    title = item.find('./{http://www.itunes.com/dtds/podcast-1.0.dtd}subtitle').text # <title> tag has unecessary padding strings
    author = item.find('./{http://www.itunes.com/dtds/podcast-1.0.dtd}author').text
    # Get date as XBMC wants it
    pub_date = item.find('./pubDate').text[:-6]
    try:
        date = time.strptime(pub_date, "%a, %d %b %Y %H:%M:%S")
    except ValueError, e:
        print '[%s] %s Could not parse date: %s' % (plugin.__plugin__, __name__, pub_date)
        print e
        date = time.localtime()
    date = time.strftime("%d.%m.%Y", date)
        
    pic = item.find('./{http://search.yahoo.com/mrss/}thumbnail').get('url')
    link = item.find('./enclosure').get('url')
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
        
        for item in fromstring(rss).findall('channel/item'):
            yield getTalkDetails(item)
