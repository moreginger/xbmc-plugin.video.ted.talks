
import re
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common

def get(html):
    """Extract talk details from talk html"""

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
        youtube_re = re.compile('https?://.*?youtube.com/.*?/([^/?]+)')
        vimeo_re = re.compile('https?://.*?vimeo.com/.*?/([^/?]+)')
        for link in xbmc_common.parseDOM(html, 'iframe', ret='src'):
            match = youtube_re.match(link)
            if match:
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (match.group(1))
                break
            match = vimeo_re.match(link)
            if match:
                url = 'plugin://plugin.video.vimeo?action=play_video&videoid=%s' % (match.group(1))
                break

    # TODO if not url: display error

    return url, title, speaker, plot
