
import re
import json
import YDStreamExtractor
from .. import settings

class Talk:

    def __init__(self, get_html):
        self.fetch = get_html  # text

    def URL(self, *path):
        return '/'.join([settings.__ted_url__, *path])

    def fetch_NEXT_DATA(self, url):
        m = '<script id="__NEXT_DATA__"[^>]*>(.+?)<\/script>'
        m = re.compile(m, re.S).search(self.fetch(url))
        return json.loads(m.group(1) if bool(m) else '{}')
        
    ## fetch the information for a single TED talk
    def fetch_talk(self, url, season=None, episode=None, tvshow=None):

        def DATE(s):
            return '.'.join(reversed(s.split('-')))

        def DATE2(s):
            return s.replace('T', ' ').replace('Z', '')

        data = self.fetch_NEXT_DATA(url)
        videoData = data['props']['pageProps']['videoData']
        playerData = json.loads(videoData['playerData'])
        data = None # no need to reference data anymore

        vidinfo = {
            'title': videoData['title'],
            'duration': videoData['duration'],
            'date': DATE(videoData['recordedOn']),
            'aired': videoData['recordedOn'],
            'dateadded': DATE2(videoData['publishedAt']),
            'plot': videoData['description'],
            'genre' : playerData.get('event'),
            'mediatype' : 'video',
            'url': self.URL('talks', videoData['slug'])
        }
        if bool(season):
            vidinfo['season'] = int(season)
        if bool(episode):
            vidinfo['episode'] = int(episode)
            vidinfo['mediatype'] = 'episode'
        if bool(season) or bool(episode):
            vidinfo['tvshowtitle'] = playerData.get('event')
        if tvshow:
            vidinfo['tvshowtitle'] = tvshow

        artwork = videoData.get('primaryImageSet', [])
        artwork = artwork[0].get('url') if artwork else None
        artwork = { 'icon': artwork, 'thumb': artwork }

        speaker = (videoData.get('speakers', {})).get('nodes',[])
        speaker = speaker[0] if speaker else {}
        speaker = {
            'name': videoData.get('presenterDisplayName'),
            'role': speaker.get('description', ''),
            'thumbnail': speaker.get('photoUrl'),
            'intro': speaker.get('whoTheyAre', ''),
            'brief': speaker.get('whyListen', ''),
            'url': self.URL('speakers', speaker.get('slug'))
        }

        stream = (playerData['resources']['hls']).get('stream')
        if stream:
            #?# remove default intro as it messes up the subtitle timing
            stream = (str(stream).split('?'))[0]
        else:
            # we don't have a url. maybe it's a youtube video
            x = playerData.get('external', {})
            if x.get('service') == 'YouTube':
                x = 'http://www.youtube.com/watch?v=%s' % (x['code'])
                x = YDStreamExtractor.getVideoInfo(x, quality=1)
                stream = x.streamURL()

        subtitles = None
        accl = settings.get_subtitle_languages()
        if accl:
            lang = playerData.get('languages', [])
            lang = [l['languageCode'] for l in lang]
            lang = [l for l in accl if l in lang]
            id = playerData['id']
            L0 = lang[0] if lang else 'en'
            subtitles = self.URL('talks/subtitles/id/%s/lang/%s' % (id, L0))

        ''' # #?# perhaps support a list of subtitles in the future
        def collect_subtitles(subtitles, languages):
            def sub(l):
                for s in subtitles:
                    if s.get('code', '') == l:
                        return s.get('webvtt')
                return None
            return [sub(l) for l in languages if sub(l)]
        '''
        
        metadata = (playerData['resources']['hls']).get('metadata')
        if metadata:
            #?# remove default intro to match the video stream
            metadata = (str(metadata).split('?'))[0]
            if accl:
                metadata = json.loads(self.fetch(metadata))
                for s in metadata.get('subtitles', []):
                    if s.get('code', '') == L0:
                        if bool(s.get('webvtt','')):
                            subtitles = s.get('webvtt','')
                            break

        return stream, subtitles, vidinfo, artwork, speaker

    ## fetch the subtitles, cache locally in srt format
    def cache_subtitles(self, url):

        def T(t):
            ms = t % 1000
            sc = (t / 1000) % 60
            mn = (t / 60000) % 60
            hr = t / 3600000
            return '%02d:%02d:%02d,%03d' % (hr, mn, sc, ms)

        cache_file = '/tmp/TED_talk_subs.srt'

        try:
            data = self.fetch(url)
            if data:
                data = json.loads(data)

            # always create to clear out any previous subtitles
            with open(cache_file, 'w', encoding='utf-8') as fp:
                if data:
                    for i, p in enumerate(data.get('captions', [])):
                        s = p['startTime']
                        e = s + p['duration']
                        c = p['content']
                        fp.write('%d\n%s --> %s\n%s\n\n' % (i+1, T(s),T(e),c))
        except:
            data = None

        return cache_file if data else None

    # retrieve a playlist and list videos
    def fetch_playlist(self, url):
        playlist = self.fetch_NEXT_DATA(url)
        playlist = playlist['props']['pageProps']['playlist']
        title = playlist['title']
        plot  = playlist.get('description')
        url = self.URL('playlists', playlist['id'], playlist['slug'])
        thumb = playlist.get('primaryImageSet', [])
        thumb = thumb[0].get('url') if thumb else ''
        group = {
            'title': title,
            'plot': plot,
            'thumb': thumb,
            'url': url
        }
        videos = playlist.get('videos', {})
        playlist = None # no need to reference playlist anymore
        ##?## a,b could indicate if the video list is complete
        a = int(videos.get('totalCount', 0))
        b = int(videos.get('pageInfo', {}).get('endCursor', 0))
        yield group, a, b
        for n, li in enumerate(videos.get('nodes', [])):
            url = li.get('canonicalUrl','')
            yield self.fetch_talk(url, '1', n+1, title)
