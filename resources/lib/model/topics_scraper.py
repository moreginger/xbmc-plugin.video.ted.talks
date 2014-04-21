from url_constants import URLTED, URLTOPICS
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common

class Topics:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get_topics(self):
        html = self.get_HTML(URLTOPICS)
        for topic_div in xbmc_common.parseDOM(html, 'div', {'class':'topics__list__topic'}):
            title = xbmc_common.parseDOM(topic_div, 'a')[0]
            link = xbmc_common.parseDOM(topic_div, 'a', ret='href')[0]
            yield title, URLTED + link


    def get_talks(self, url):
        url = url + "?page=%s"
        page_index = 1
        html = self.get_HTML(url % (page_index))
        
        # Have to know when to stop paging, see condition for loop exit below.
        found_titles = set()
        found_on_last_page = 0

        while True:
            talk_box = xbmc_common.parseDOM(html, 'div', {'class':'box talks'})[0]
            talk_list = xbmc_common.parseDOM(talk_box, 'ul')[0]
            found_before = len(found_titles)
            for talk in xbmc_common.parseDOM(talk_list, 'li'):
                title = xbmc_common.parseDOM(talk, 'a', ret='title')[0].strip()
                if title not in found_titles:
                    found_titles.add(title)
                    link = xbmc_common.parseDOM(talk, 'a', ret='href')[0]
                    for img_link in xbmc_common.parseDOM(talk, 'img', ret='src'):
                        if 'images.ted.com' in img_link:
                            yield title, URLTED + link, img_link
                            break

            # Results on last page == results on (last page + 1), _not_ 0 as you might hope.
            # The second clause allows us to skip looking at last page + 1 if the last page contains
            # fewer results than that before it; which is usually but not always the case.
            found_on_this_page = len(found_titles) - found_before
            if found_on_this_page and found_on_this_page >= found_on_last_page:
                page_index += 1
                found_on_last_page = found_on_this_page
                html = self.get_HTML(url % (page_index))
            else:
                break
