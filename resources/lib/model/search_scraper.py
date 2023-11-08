import html
import html5lib
import urllib.parse
import re

from .. import settings

class Search:

    def __init__(self, get_html):
        self.fetch = get_html  #text

    def __AtoBofC__(self, html):
        # e.g. "331 - 360 of 333 results"
        m = re.search(r'\D(\d+) - (\d+) of (\d+) results', html, re.I | re.A)
        if bool(m):
            return int(m.group(1)), int(m.group(2)), int(m.group(3))
        # two spaces at the moment i.e. "1  result"
        m = re.search(r'\D(\d+) +results', html, re.I | re.A)
        if bool(m):
            return 1, int(m.group(1)), int(m.group(1))
        return 1, 1, 1

    def URL(self, search_string, page, category):
        return '%s/search?cat=%s&q=%s&page=%s' % (
            settings.__ted_url__,
            'playlists' if category == 'p' else 'videos',
            search_string,
            page)

    def fetch_search(self, search_string, page, category):
        '''
        Yields number of results left to show after this page,
        then tuples of title, link, img for results on this page.
        '''
        doublecheck = '/playlists/' if category == 'p' else '/talks/'
        search_string = urllib.parse.quote_plus(search_string)
        content = self.fetch(self.URL(search_string, page, category))
        results = html5lib.parse(content, namespaceHTMLElements=False)
        results = results.findall(".//article[@class='m1 search__result']")

        a, b, c = self.__AtoBofC__(content) 
        yield a, b, c

        for r in results:
            url = r.find('.//a[@href]').attrib['href']
            if not url.startswith(doublecheck):
                continue
            title = html.unescape(r.find('.//h3/a').text.strip())
            thumb = r.find('.//img[@src]').attrib['src']
            desc = r.findall(".//div[@class='search__result__description m4']")
            if desc:
                for br in desc[0].findall('.//br'):
                    br.tail = '\n' + (br.tail.lstrip() if br.tail else '')
                for p in desc[0].findall('.//p'):
                    p.tail = '\n\n' + (p.tail.lstrip() if p.tail else '')
                desc = ''.join(desc[0].itertext()).strip()
            yield title, settings.__ted_url__ + url, thumb, desc or ''
