import urllib
from url_constants import URLSEARCH
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common
import re

__results_count_re__ = re.compile(r'\d+-(\d+) of (\d+) results')

class Search:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get_talks_for_search(self, search_string, page_index):
        '''
        Yields number of results left to show after this page,
        then tuples of title, link, img for results on this page.
        '''
        # TODO Read result count and use for paging control
        
        search_string = urllib.quote_plus(search_string)
        html = self.get_HTML(URLSEARCH % (search_string, page_index))
        
        yield self.results_remaining(html)

        results = xbmc_common.parseDOM(html, 'div', {'class': 'result video'})
        for result in results:
            div = xbmc_common.parseDOM(result, 'div', {'class': 'thumb'})[0]

            title = xbmc_common.parseDOM(div, 'img', ret='alt')[0].strip()
            link = xbmc_common.parseDOM(div, 'a', ret='href')[0]
            img = xbmc_common.parseDOM(div, 'img', ret='src')[0]
            yield title, link, img

    def results_remaining(self, html):
        results_count_div = xbmc_common.parseDOM(html, 'div', {'class': 'search-title clearfix'})
        if results_count_div:
            results_count = xbmc_common.parseDOM(results_count_div[0], 'span')
            if results_count:
                results_count_match = __results_count_re__.match(results_count[0])
                if results_count_match:
                    return int(results_count_match.group(2)) - int(results_count_match.group(1))
               
        # We don't know so just make sure that it is positive so that we keep paging.
        yield 1
