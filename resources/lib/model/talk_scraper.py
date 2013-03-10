
import re
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions.parseDOM as parseDOM

class Talk:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get(self, url):
        html = self.get_HTML(url)
        headline = parseDOM(html, 'span', attrs={'id':'altHeadline'})[0].split(':', 1)
        speaker = headline[0].strip()
        title = headline[1].strip()
        plot = parseDOM(html, 'p', attrs={'id':'tagline'})[0]

        url = ""
        link_re = re.compile('http://download.ted.com/talks/.+.mp4')
        for link in parseDOM(html, 'a', ret='href'):
            if link_re.match(link):
                url = link
                break

        return url, title, speaker, plot
