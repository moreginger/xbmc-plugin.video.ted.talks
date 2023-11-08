
import re
import json
import time

from .. import settings

class Topics:

    def __init__(self, get_html):
        self.fetch = get_html  # text

    def URL(self, *parts):
        return '/'.join([settings.__ted_url__, *parts]) 

    def fetch_json(self, url):
        m = '<script id="__NEXT_DATA__"[^>]*>(.+?)<\/script>'
        m = re.search(m, self.fetch(url), re.S)
        data = json.loads(m.group(1) if bool(m) else '{}')
        return data.get('props', {}).get('pageProps', {})

    def fetch_topics(self):
        topics = self.fetch_json(self.URL('topics')).get('list', [])
        topics = sorted(topics, key=lambda k: k.get('letter', ''))
        for letter in topics:
            for topic in letter.get('items',[]):
                yield topic.get('name', ''), topic.get('slug', '')

    def fetch_featured(self, topic_slug):
        data = self.fetch_json(self.URL('topics', topic_slug))
        name = data.get('name','')
        playlists = data.get('playlists', [])
        for p in playlists:
            thumb = p.get('primaryImageSet', [])
            thumb = thumb[0].get('url') if thumb else None
            yield 'p', {
                'tag': name,
                'title': p.get('title'),
                'thumb': thumb,
                'plot': p.get('description', ''),
                'count': int(p.get('videos', {}).get('totalCount', 0)),
                'mediatype': 'tvshow',
                'author': p.get('author', ''),
                'url': self.URL('playlists', p.get('id'), p.get('slug'))
            }
        talks = data.get('talks', [])
        for t in talks:
            thumb = t.get('primaryImageSet', [])
            thumb = thumb[0].get('url') if thumb else None
            yield 't', {
                'tag': name,
                'title': t.get('title'),
                'thumb': thumb,
                'plot': t.get('description', ''),
                'duration': int(t.get('duration', 0)),
                'mediatype': 'video',
                'author': t.get('presenterDisplayName', ''),
                'url': t.get('canonicalUrl')
            }
