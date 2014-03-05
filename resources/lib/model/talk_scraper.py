
import re
# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common
import httplib
import urlparse
import json
import re


def get(html, video_quality='320kbps'):
    """Extract talk details from talk html
       @param video_quality string in form '\d+kbps' that should match one of the provided TED bitrates.
    """

    speaker = xbmc_common.parseDOM(html, 'a', attrs={'class':'talk-hero__speaker__link'})[0].strip()
    title = xbmc_common.parseDOM(html, 'div', attrs={'class':'talk-hero__title'})[0].strip()
    plot = xbmc_common.parseDOM(html, 'p', attrs={'class':'talk-description'})[0]

    init_script = [script for script in xbmc_common.parseDOM(html, 'script') if '"talkPage.init"' in script][0]
    init_json = json.loads(re.compile(r'q[(]"talkPage.init",(.+)[)]').search(init_script).group(1))
    url = init_json['talks'][0]['resources']['h264'][0]['file']

    # We could confirm these URLs exist from the DOM (with difficulty) but seems likely to break
    if url and not video_quality == '320kbps':
        url_custom = url.replace("-320k.mp4", "-%sk.mp4" % (video_quality.split('k')[0]))

        # Test resource exists
        url_custom_parsed = urlparse.urlparse(url_custom)
        h = httplib.HTTPConnection(url_custom_parsed.netloc)
        h.request('HEAD', url_custom_parsed.path)
        response = h.getresponse()
        h.close()
        if response.status / 100 < 4:
            url = url_custom

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
