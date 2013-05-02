import re
from BeautifulSoup import SoupStrainer, MinimalSoup as BeautifulSoup
from model.url_constants import URLTED
import model.subtitles_scraper as subtitles_scraper
import model.talk_scraper as talk_scraper

# MAIN URLS
URLSPEAKERS = 'http://www.ted.com/speakers/atoz/page/'
URLSEARCH = 'http://www.ted.com/search?q=%s/page/'


def getNavItems(html):
    """self.navItems={'next':url, 'previous':url, 'selected':pagenumberasaninteger}"""
    navItems = {'next':None, 'previous':None, 'selected':1}
    paginationContainer = SoupStrainer(attrs={'class':re.compile('pagination')})
    for aTag in BeautifulSoup(html, parseOnlyThese=paginationContainer).findAll('a'):
        if aTag.has_key('class'):
            if aTag['class'] == 'next':
                navItems['next'] = URLTED + aTag['href']
            elif aTag['class'] == 'prev':
                navItems['previous'] = URLTED + aTag['href']
            elif aTag['class'] == 'selected':
                navItems['selected'] = int(aTag.string)
    return navItems


class TedTalks:

    def __init__(self, getHTML, logger):
        self.getHTML = getHTML
        self.logger = logger

    def getVideoDetails(self, url, video_quality, subs_language=None):
        talk_html = self.getHTML(url)
        video_url, title, speaker, plot = talk_scraper.get(talk_html, video_quality)

        subs = None
        if subs_language:
            subs = subtitles_scraper.get_subtitles_for_talk(talk_html, subs_language, self.logger)

        return title, video_url, subs, {'Director':speaker, 'Genre':'TED', 'Plot':plot, 'PlotOutline':plot}

