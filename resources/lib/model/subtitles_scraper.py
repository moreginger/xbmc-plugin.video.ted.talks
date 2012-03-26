'''
Inspired by code of Esteban Ordano

http://estebanordano.com/ted-talks-download-subtitles/
http://estebanordano.com.ar/wp-content/uploads/2010/01/TEDTalkSubtitles.py_.zip
'''
import simplejson
import urllib
import re

def format_time(time):
    millis = time % 1000
    seconds = (time / 1000) % 60
    minutes = (time / 60000) % 60
    hours = (time / 3600000)
    return '%02d:%02d:%02d,%03d' % (hours, minutes, seconds, millis)

def get_languages(languages):
    '''
    languages Escaped languages param from flashVars
    '''
    language_code_re = re.compile('"LanguageCode":"(\w+)"')
    matches = filter(None, [language_code_re.search(param) for param in urllib.unquote(languages).split(',')])
    return [m.group(1) for m in matches]

def get_flashvars(soup):
    '''
    Get flashVars for a talk.
    Blow up if we can't find it or if we fail to parse.
    returns dict of values, no guarantees are made about which values are present.
    '''
    flashVars_re = re.compile('flashVars = {([^}]+)}')
    flash_script = soup.find('script', text=flashVars_re)
    if not flash_script:
        raise Exception('Could not find flashVars')
    flashVars = flashVars_re.search(flash_script.string).group(1)
    flashVar_re = re.compile('\s*(\w+):(.+),?')
    matches = filter(None, [flashVar_re.match(l) for l in flashVars.split('\n')])
    return dict([(m.group(1).encode('ascii'), m.group(2).encode('ascii')) for m in matches])

def get_subtitles(talk_id, language):
    url = 'http://www.ted.com/talks/subtitles/id/%s/lang/%s' % (talk_id, language)
    return get_subtitles_for_url(url)
        
def get_subtitles_for_url(url):
    s = urllib.urlopen(url)
    try:
        json = simplejson.load(s)
    finally:
        s.close()

    captions = []
    for caption in json['captions']:
        captions += [{'start': caption['startTime'], 'duration': caption['duration'], 'content': caption['content']}]
    return captions