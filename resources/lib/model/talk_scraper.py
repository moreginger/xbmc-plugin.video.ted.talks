# 2022-03 Convert to use regular expressions
import json
import re


def get_talk(html, logger):
    '''Extract talk details from talk html
    '''

    init_scripts = re.compile(
        '<script id="__NEXT_DATA__"[^>]*>(.+?)<\/script>', re.DOTALL).search(html).group(1)
    if not init_scripts:
        raise Exception('Could not find init_scripts.')

    init_json = json.loads(str(init_scripts), strict=False)
    video_json = init_json['props']['pageProps']['videoData']
    player_raw = video_json['playerData']
    player_json = json.loads(str(player_raw), strict=False)

    url = player_json['resources']['hls']['stream']
    # Remove default intro as it messes up the subtitle timing
    pos_of_question_mark = str(url).find('?intro_master_id=')
    if pos_of_question_mark >= 0:
        url = str(url)[0:pos_of_question_mark]

    # Scrape metadata from talk if possible.
    title, speaker, plot = '', '', ''
    try:
        try:
            title = str(player_json['title'])
        except Exception as e:
            logger(msg='Could not get talk title: %s' % (e), level='debug')
            pass

        try:
            speaker = str(player_json['speaker'])
        except Exception as e:
            logger(msg='Could not get talk speaker: %s' % (e), level='debug')
            pass

        try:
            plot = str(video_json['description'])
        except Exception as e:
            logger(msg='Could not get talk plot: %s' % (e), level='debug')
            pass
    except e:
        logger('There was an exception scraping metadata for a talk. %s', e)

    if (not title or not speaker or not plot):
        short_message = 'Some metadata for the talk could not be found'
        detailed_message = '%s. title=%s, speaker=%s, plot=%s' % (
            short_message, title, speaker, plot)
        logger(msg=detailed_message, friendly_message=short_message)

    return url, title, speaker, plot, player_json
