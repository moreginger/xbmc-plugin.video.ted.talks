import html5lib
import json
import requests


def get(html, logger, video_quality='180kbps'):
    '''Extract talk details from talk html
       @param video_quality string in form '\\d+kbps' that should match one of the provided TED bitrates.
    '''

    init_scripts = html5lib.parse(html, namespaceHTMLElements=False).findall(".//script[@data-spec='q']")
    init_scripts = [script.text for script in init_scripts if '"talkPage.init"' in script.text]
    if init_scripts:
        # let's do this some other way
        init_scripts_start_pos = str(init_scripts).find('{')
        init_scripts = str(init_scripts)[init_scripts_start_pos:]
        init_scripts = init_scripts + '}'

        # let's remove some json breaking invalid characters
        init_scripts = init_scripts.replace('\\n\\t', '')
        init_scripts = init_scripts.replace("\\n})']", '')
        init_scripts = init_scripts.replace('\\\\"', '')
        init_scripts = init_scripts.replace('\\', '')
        init_scripts = init_scripts[:-4]

        init_json = json.loads(str(init_scripts), strict=False)
        talk_json = init_json['__INITIAL_DATA__']['talks'][0]
        
        title = talk_json['player_talks'][0]['title']
        speaker = talk_json['player_talks'][0]['speaker']
        plot = talk_json['description']

        url = talk_json['downloads']['nativeDownloads']['medium']
        url = url[0:url.find('?')]

        # Attempt to switch to user-specified bitrate.
        url_custom = url.replace('.mp4', '-%sk.mp4' % (video_quality.split('k')[0]))
        if requests.head(url_custom).ok:
            url = url_custom
        else:
            logger("Could not create URL for bitrate '%s' from '%s'." % (video_quality, url))

        return url, title, speaker, plot, talk_json
    else:
        raise Exception('Could not parse HTML:\n%s' % (html))
