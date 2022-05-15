# 2022-03 Convert to use regular expressions
import json
import requests
import re
import sys
import xbmc

# get() used in Kodi 18.x
def get(html, logger, video_quality='180kbps'):
    '''Extract talk details from talk html
       @param video_quality string in form '\\d+kbps' that should match one of the provided TED bitrates.
    '''

    init_scripts = re.compile('<script id="__NEXT_DATA__"[^>]*>(.+?)<\/script>', re.DOTALL).search(html).group(1)
    xbmc.log(msg='%s = %s' % ('init_scripts', str(init_scripts)), level=xbmc.LOGDEBUG)

    if not init_scripts:
        raise Exception('Could not parse HTML.')

    # Parse playerData before init_scripts content is altered
    player_raw = re.compile('"playerData":"(\{.*[\}]+?)"', re.DOTALL).search(init_scripts).group(1)
    xbmc.log(msg='%s = %s' % ('player_raw', str(player_raw)), level=xbmc.LOGDEBUG)

    if not player_raw:
        raise Exception('Could not parse HTML for playerData.')

    # Remove some json breaking invalid characters
    player_raw = player_raw.replace('\\"', '"')
    player_raw = player_raw.replace('\\\\', '\\')
    player_raw = player_raw.replace('\\\\"', '\\"')
    xbmc.log(msg='%s = %s' % ('player_raw altered', str(player_raw)), level=xbmc.LOGDEBUG)
    player_json = json.loads(player_raw)

    # let's remove some json breaking invalid characters
    init_scripts = init_scripts.replace('\\n\\t', '')
    init_scripts = init_scripts.replace("\\n})']", '')
    init_scripts = init_scripts.replace("\\\\", '\\"')
    init_scripts = init_scripts.replace("']}", '')
    xbmc.log(msg='%s = %s' % ('init_scripts altered', init_scripts), level=xbmc.LOGDEBUG)

    init_json = json.loads(str(init_scripts), strict=False)
    talk_json = init_json['props']['pageProps']['videoData']

    try:
        title = str(talk_json['title']).decode('ascii', 'ignore')
    except:
        title = ''
    xbmc.log(msg='%s = %s' % ('title', title), level=xbmc.LOGDEBUG)

    try:
        speaker = str(player_json['speaker']).decode('ascii', 'ignore')
    except:
        speaker = ''
    xbmc.log(msg='%s = %s' % ('speaker', speaker), level=xbmc.LOGDEBUG)

    #xbmc.log(msg='%s = %s' % ('sys.version_info.major', sys.version_info.major), level=xbmc.LOGDEBUG)
    #if sys.version_info.major < 3:
    #    url = player_json['resources']['h264'][0]['file']
    #else:
    #    url = player_json['resources']['hls']['stream']
    url = player_json['resources']['hls']['stream']
    xbmc.log(msg='%s = %s' % ('url', url), level=xbmc.LOGDEBUG)

    # Remove default intro as it messes up the subtitle timing
    pos_of_question_mark = str(url).find('?')
    if pos_of_question_mark >= 0:
        url = str(url)[0:pos_of_question_mark]
    xbmc.log(msg='%s = %s' % ('url intro removed', url), level=xbmc.LOGDEBUG)

    try:
        plot = str(talk_json['description']).decode('ascii', 'ignore')
    except:
        plot = ''
    xbmc.log(msg='%s = %s' % ('plot', plot), level=xbmc.LOGDEBUG)

    return url, title, speaker, plot, talk_json, player_json

# get_talk() used in Kodi 19+
def get_talk(html, logger):
    url, title, speaker, plot, talk_json, player_json = get(html, logger)
    return url, title, speaker, plot, talk_json, player_json
