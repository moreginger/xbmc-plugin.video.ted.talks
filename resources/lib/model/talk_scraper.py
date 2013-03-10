
import re
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common

class Talk:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get(self, url):
        html = self.get_HTML(url)
        headline = xbmc_common.parseDOM(html, 'span', attrs={'id':'altHeadline'})[0].split(':', 1)
        speaker = headline[0].strip()
        title = headline[1].strip()
        plot = xbmc_common.parseDOM(html, 'p', attrs={'id':'tagline'})[0]

        url = None
        if not url:
            link_re = re.compile('http://download.ted.com/talks/.+.mp4')
            for link in xbmc_common.parseDOM(html, 'a', ret='href'):
                if link_re.match(link):
                    url = link
                    break

        if not url:
            link_re = re.compile('https?://(www.)?youtube.com/.*?/([^/?]+)')
            for link in xbmc_common.parseDOM(html, 'iframe', ret='src'):
                match = link_re.match(link)
                if match:
                    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(2))
                    break

        # TODO if not url: display error
        # TODO vimeo

        return url, title, speaker, plot
