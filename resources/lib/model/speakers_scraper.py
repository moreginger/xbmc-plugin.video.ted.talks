from url_constants import URLSPEAKERS
from url_constants import URLTED
from util import resizeImage
from BeautifulSoup import SoupStrainer, MinimalSoup as BeautifulSoup
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common
import re

class Speakers:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get_speakers_for_letter(self, char):
        '''
        First yields the speaker count, or 0 if unknown.
        After that yields tuples of title, link, img.
        '''
        page_index = 1
        html = self.get_HTML(URLSPEAKERS % (page_index, char))

        speaker_count = 0
        for h2 in xbmc_common.parseDOM(html, 'h2'):
            if 'speakers whose Last Name begins with' in h2:
                spans = xbmc_common.parseDOM(h2, 'span')
                if spans:
                    try:
                        speaker_count = int(spans[-1].strip())
                    except ValueError:
                        pass

        yield speaker_count

        # Have to know when to stop paging, see condition for loop exit below.
        found_titles = set()
        found_on_last_page = 0

        while True:
            dls = xbmc_common.parseDOM(html, 'dl', {'class': 'speakerMedallion'})
            found_before = len(found_titles)
            for dl in dls:
                dt = xbmc_common.parseDOM(dl, 'dt')[0]
                title = xbmc_common.parseDOM(dt, 'img', ret='alt')[0].strip()
                if title not in found_titles:
                    found_titles.add(title)
                    link = xbmc_common.parseDOM(dt, 'a', ret='href')[0]
                    img = xbmc_common.parseDOM(dt, 'img', ret='src')[0]
                    yield title, URLTED + link, img

            # Results on last page == results on (last page + 1), _not_ 0 as you might hope.
            # The second clause allows us to skip looking at last page + 1 if the last page contains
            # fewer results than that before it; which is usually but not always the case.
            found_on_this_page = len(found_titles) - found_before
            if found_on_this_page and found_on_this_page >= found_on_last_page:
                page_index += 1
                found_on_last_page = found_on_this_page
                html = self.get_HTML(URLSPEAKERS % (page_index, char))
            else:
                break
            
    def get_talks_for_speaker(self, url):
        '''
        Yields tuples of title, link, img.
        '''
        html = self.get_HTML(url)
        talkContainer = SoupStrainer(attrs={'class':re.compile('box clearfix')})
        for talk in BeautifulSoup(html, parseOnlyThese=talkContainer):
            title = talk.h4.a.string
            link = URLTED + talk.dt.a['href']
            pic = resizeImage(talk.find('img', attrs={'src':re.compile('.+?\.jpg')})['src'])
            yield title, link, pic
