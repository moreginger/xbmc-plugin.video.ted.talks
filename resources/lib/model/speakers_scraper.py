
import html5lib

from .. import settings
from .talk_scraper import Talk

class Speakers:

    def __init__(self, get_html):
        self.fetch = get_html #text

    def URL(self, *path):
        return '/'.join([p.lstrip('/') for p in [settings.__ted_url__, *path]])

    def __get_page__(self, index):
        data = self.fetch(self.URL('speakers?page=%s' % (index)))
        return html5lib.parse(data, namespaceHTMLElements=False)

    def __get_page_count__(self, dom):
        data = dom.findall(".//a[@class='pagination__item pagination__link']")
        return int(data[-1].text)

    def get_speaker_page_count(self):
        return self.__get_page_count__(self.__get_page__(1))

    def get_1st_speaker_of(self, page):
        '''
        Return the name of the first speaker for the given page
        '''
        dom = self.__get_page__(page)
        R = ".//a[@class='results__result media media--sm-v m4']//h4"
        who = dom.findall(R)
        if who:
            for br in who[0].findall('.//br'):
                br.tail = ' ' + (br.tail.lstrip() if br.tail else '')
            who = ''.join(who[0].itertext()).strip()
        return who or 'missing speaker'

    def get_speakers_for_pages(self, pages):
        '''
        First yields the number of pages of speakers.
        After that yields tuples of title, link, img, tagline.
        '''
        dom = self.__get_page__(pages[0])
        yield self.__get_page_count__(dom)

        for p in pages:
            if not dom:
                dom = self.__get_page__(p)
            R = ".//a[@class='results__result media media--sm-v m4']"
            for r in dom.findall(R):
                url = self.URL(r.attrib['href'])
                who = r.findall('.//h4')
                if who:
                    for br in who[0].findall('.//br'):
                        br.tail = ' ' + (br.tail.lstrip() if br.tail else '')
                    who = ''.join(who[0].itertext()).strip()
                img = r.findall('.//img[@src]')
                img = img[0].attrib['src'] if img else None
                tag = r.findall('.//strong')
                tag = tag[0].text.strip() if tag and tag[0].text else ''
                yield who or 'missing speaker', url, img, tag
            dom = None

    def get_talks_for_speaker(self, url):
        '''
        Yields tuples of title, link, img.
        '''
        dom = html5lib.parse(self.fetch(url), namespaceHTMLElements=False)

        # speaker info
        def T(t): return t[0].text.strip() if t and t[0].text else ''
        speaker = T(dom.findall(".//*[@class='h2 profile-header__name']"))
        tagline = T(dom.findall(".//*[@class='p2 profile-header__summary']"))
        thumb =dom.findall(".//div[@class='profile-header__thumb']//img[@src]")
        thumb = thumb[0].attrib['src'] if thumb else None
        intro = T(dom.findall(".//div[@class='profile-intro']"))
        extra = dom.findall(".//div[@class='section section--minor']")
        if extra:
            for br in extra[0].findall('.//br'):
                br.tail = '\n' + (br.tail.lstrip() if br.tail else '')
            for p in extra[0].findall('.//p'):
                p.tail = '\n\n' + (p.tail.lstrip() if p.tail else '')
            extra = ''.join(extra[0].itertext()).strip()
        yield speaker, thumb, tagline, intro, extra or ''

        # talks info
        talk = Talk(self.fetch)
        for t in dom.findall(".//div[@class='talk-link']"):
            url = t.find('.//a[@href]').attrib['href']
            #thumb = talk.find('.//img[@src]').attrib['src']
            #title = T([talk.find(".//div[@class='media__message']//a")])
            yield talk.fetch_talk(self.URL(url))
