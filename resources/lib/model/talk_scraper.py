import httplib
import json
import m3u8
import re
import urlparse

# Custom xbmc thing for fast parsing. Can't rely on lxml being available as of 2012-03.
import CommonFunctions as xbmc_common


def get(html):
    """Extract talk details from talk html
    """
    init_scripts = [script for script in xbmc_common.parseDOM(html, 'script') if '"talkPage.init"' in script]
    init_json = json.loads(re.compile(r'q[(]"talkPage.init",(.+)[)]').search(init_scripts[0]).group(1))
    talk_json = init_json['talks'][0]
    hls = talk_json['resources']['hls']
    url = hls['stream']
    title = talk_json['title']
    speaker = talk_json['speaker']
    plot = xbmc_common.parseDOM(html, 'p', attrs={'class':'talk-description'})[0]

    return url, title, speaker, plot, talk_json
