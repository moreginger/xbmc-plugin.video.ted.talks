# 2022-03 Convert to use regular expressions
import json
import requests
import re
import sys

def get_talk(html, logger):
    '''Extract talk details from talk html
    '''

    init_scripts = re.compile('<script id="__NEXT_DATA__"[^>]*>(.+?)<\/script>', re.DOTALL).search(html).group(1)
    if not init_scripts:
        raise Exception('Could not find init_scripts.')
    
    logger(msg='%s = %s' % ('init_scripts', str(init_scripts)), level='debug')

    player_raw = re.compile('"playerData":"(\{.*[\}]+?)"', re.DOTALL).search(init_scripts).group(1)
    if not player_raw:
        raise Exception('Could not find playerData.')

    # Remove some json breaking invalid characters
    player_raw = player_raw.replace('\\"', '"')
    player_raw = player_raw.replace('\\\\', '\\')
    player_raw = player_raw.replace('\\\\"', '\\"')
    logger(msg='%s = %s' % ('player_raw altered', str(player_raw)), level='debug')
    player_json = json.loads(player_raw)

    url = player_json['resources']['hls']['stream']
    # Remove default intro as it messes up the subtitle timing
    pos_of_question_mark = str(url).find('?')
    if pos_of_question_mark >= 0:
        url = str(url)[0:pos_of_question_mark]
    logger(msg='%s = %s' % ('url', url), level='debug')

    # Scrape metadata from talk...

    # Remove some more json breaking invalid characters
    init_scripts = init_scripts.replace('\\n\\t', '')
    init_scripts = init_scripts.replace("\\n})']", '')
    init_scripts = init_scripts.replace("']}", '')

    try:
        init_json = json.loads(str(init_scripts), strict=False)
        talk_json = init_json['props']['pageProps']['videoData']

        try:
            title = str(talk_json['title']).decode('ascii', 'ignore')
        except:
            title = ''

        try:
            speaker = str(player_json['speaker']).decode('ascii', 'ignore')
        except:
            speaker = ''

        try:
            plot = str(talk_json['description']).decode('ascii', 'ignore')
        except:
            plot = ''
    except e:
        logger('There was an exception scraping metadata for a talk. %s', e)

    if (not title or not speaker or not plot):
        msg = 'Some metadata for the talk could not be found.'
        logger(msg=msg, friendly_message=msg)

    return url, title, speaker, plot, player_json
