import itertools
import os
import sys
import time
import urllib.parse
import re

import xbmc
import xbmcgui
import xbmcplugin

from . import settings

from .model.fetcher import Fetcher
from .model.talk_scraper import Talk
from .model.search_scraper import Search
from .model.rss_scraper import NewTalksRss
from .model.speakers_scraper import Speakers
from .model.series_scraper import Series
from .model.topics_scraper import Topics

__handle__ = int(sys.argv[1])

def logger(gnarly_message, friendly_message=None, level='info'):
    settings.report(gnarly_message, friendly_message, level)

class UI:

    def __init__(self, fetcher):
        self.fetcher = fetcher

    def localized_string(self, id):
        return settings.get_localized_string(id)

    def quote_for_url(self, v):
        return urllib.parse.quote_plus(v.encode('ascii', 'ignore'))

    def create_action_url(self, mode, url=None, args={}):

        args['mode'] = mode
        if url:
            args['url'] = url
        args = [k + '=' + self.quote_for_url(v) for k, v in args.items()]
        return sys.argv[0] + '?' + '&'.join(args)

    def create_ListFldr(self, title, art=None, desc=None):

        li = xbmcgui.ListItem(title, offscreen=True)
        if bool(art):
            if type(art) == dict:
                li.setArt(art)
            else:
                li.setArt({'thumb': art, 'icon': art})
        if bool(desc):
            if type(desc) == dict:
                li.setInfo('video', desc)
            else:
                li.setInfo('video', {'title': title, 'plot': desc})
        li.addContextMenuItems([])
        li.setProperty('IsPlayable', 'false')
        li.setIsFolder(True)
        return li

    def create_ListItem(self, urlp, subp, vid, art, spkr):
        # missing path, try to substitute with the talk page
        if not bool(urlp):
            urlp = vid.get('url','')
        li = xbmcgui.ListItem(vid.get('title'), path=urlp, offscreen=True)
        #li.setSubtitles([subp] if subp else [])
        self.set_subtitles(li, subp)
        if spkr:
            spkr.pop('intro', None)
            spkr.pop('brief', None)
            spkr.pop('url', None)
            li.setCast([spkr])
        if art:
            li.setArt(art)
        if 'duration' in vid:
            li.addStreamInfo('video', {'duration': vid['duration']})
        vid.pop('url', None)
        li.setInfo(type='video', infoLabels=vid)
        li.setProperty('IsPlayable', 'true')
        return li

    def subtitles_needs_reformatting(self, subp):
       return not (subp.find('/talks/subtitles/id/') < 0)
   
    def set_subtitles(self, li, subtitles):
        # Since there is no ListItem.getSubtitles(), we need
        # to use a phony ID to "shadow" our subtitles settings.
        if bool(subtitles):
            li.setSubtitles([subtitles])
            li.setUniqueIDs({'ExtSubtitlesPath': subtitles})

    def get_subtitles(self, li):
        # Since there is no ListItem.getSubtitles(), we need
        # to use a phony ID to "shadow" our subtitles settings.
        return li.getUniqueID('ExtSubtitlesPath')
    
    def add_DirectoryItem(self, url, listItem, isFolder=True):
        # If this is a playable item AND we don't need to fix up
        # the subtitles, then use the listItem's path to play
        # the video directly. Otherwise, use url which points to
        # the plugin's PlayVideo action.
        if not isFolder:
            if listItem.getProperty('IsPlayable') == 'true':
                subp = self.get_subtitles(listItem)
                if not self.subtitles_needs_reformatting(subp):
                    url = listItem.getPath()
        xbmcplugin.addDirectoryItem(__handle__, url, listItem, isFolder)

    def add_DirectoryItems(self, DirectoryItem_tuples):
        xbmcplugin.addDirectoryItems(__handle__, DirectoryItem_tuples)

    def end_Directory(self, content='videos',
                      sortMethod=['none'], updateListing=False):
        if content:
            xbmcplugin.setContent(__handle__, content)

        if sortMethod:
            aliases = {
                'none':  xbmcplugin.SORT_METHOD_UNSORTED,
                'date':  xbmcplugin.SORT_METHOD_DATE,
                'title': xbmcplugin.SORT_METHOD_LABEL,
                'episode': xbmcplugin.SORT_METHOD_EPISODE
            }
            if type(sortMethod) != list:
                sortMethod = [sortMethod]
            for sm in sortMethod:
                xbmcplugin.addSortMethod(__handle__, aliases.get(sm,0))

        xbmcplugin.endOfDirectory(__handle__, updateListing=updateListing)

    def showCategories(self):

        def add_category_item(title_id, blurb_id, mode, args={}):
            url = self.create_action_url(mode, args=args)
            li = self.create_ListFldr(self.localized_string(title_id),
                                      settings.__plugin_icon__,
                                      self.localized_string(blurb_id))
            self.add_DirectoryItem(url, li)

        add_category_item(30001, 30031, 'rss', {'url':'latest'})
        add_category_item(30004, 30034, 'search', {'c':'t'})
        add_category_item(30005, 30035, 'search', {'c':'p'})
        add_category_item(30002, 30032, 'people')
        add_category_item(30007, 30037, 'topics')
        add_category_item(30008, 30038, 'series')
        add_category_item(30009, 30039, 'rss')
        self.end_Directory()


class Action(object):
    '''
    Some action that can be executed by the user.
    '''
    def __init__(self, mode, required_args, *args, **kwargs):
        self.mode = mode
        self.required_args = set(required_args)

    def run(self, args):
        if self.required_args.issubset(list(args.keys())):
            self.run_internal(args)
        else:
            self.report_problem(args)

    def report_problem(self, args):
        # The theory is that this might happen for a favorite from
        # another version; though we can't be sure about the cause
        # hence vagueness in friendly message.
        msg = "Action '%s' failed. Try re-creating the item." % (self.mode)
        logger("%s\nBad arguments: %s" % (msg, args), msg)


class PlayVideoAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(PlayVideoAction,
              self).__init__('play_video', ['url'], *args, **kwargs)
        self.ui = ui

    def run_internal(self, args):
        url = args['url']
        se = args.get('se')
        ep = args.get('ep')
        talk = Talk(self.ui.fetcher.get_HTML)
        urlp, subp, vid, art, spkr = talk.fetch_talk(url, se, ep)
        if self.ui.subtitles_needs_reformatting(subp):
            subp = talk.cache_subtitles(subp)
        li = self.ui.create_ListItem(urlp, subp, vid, art, spkr)
        xbmcplugin.setResolvedUrl(__handle__, True, li)


class TalkPageAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(TalkPageAction,
              self).__init__('talkpage', ['url'], *args, **kwargs)
        self.ui = ui

    def run_internal(self, args):
        url = args['url']
        talk = Talk(self.ui.fetcher.get_HTML)
        urlp, subp, vid, art, spkr = talk.fetch_talk(url)
        #subp = talk.cache_subtitles(subp)
        url = self.ui.create_action_url('play_video', url)
        li = self.ui.create_ListItem(urlp, subp, vid, art, spkr)
        self.ui.add_DirectoryItem(url, li, False)
        self.ui.end_Directory('videos')


class PlaylistAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(PlaylistAction,
              self).__init__('playlist', ['url'], *args, **kwargs)
        self.ui = ui
        
    def run_internal(self, args):
        url = args['url']
        talk = Talk(self.ui.fetcher.get_HTML)
        generator = talk.fetch_playlist(url)
        playlist, a, b = next(itertools.islice(generator, 1))
        for urlp, subp, vid, art, spkr in generator:
            url = self.ui.create_action_url('play_video', vid.get('url'))
            li = self.ui.create_ListItem(urlp, subp, vid, art, spkr)
            self.ui.add_DirectoryItem(url, li, False)
        self.ui.end_Directory('episodes', ['episode', 'date'])


class SearchAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(SearchAction, self).__init__('search', [], *args, **kwargs)
        self.ui = ui

    def create_search_url(self, query, page, cat):
        args = { 'q': query, 'c': cat }
        return self.ui.create_action_url('search', str(page), args=args)

    def create_search_action_listitem(self, page, cat):
        def S(id): return self.ui.localized_string(id)
        icon = settings.__plugin_icon__
        cs = settings.get_current_search()
        title = S(30024) if page < 1 else S(30025) % (cs)
        label = S(30034) if cat!='p' else S(30035)
        args = { 'q': cs, 'c': cat, 'R':'1' }
        url = self.ui.create_action_url('search', str(page), args=args)
        return (url, self.ui.create_ListFldr(title, icon, label), True)

    def run_internal(self, args):
        cat = args.get('c')
        page = int(args.get('url', 1))
        search_string = args.get('q')
        R = bool(int(args.get('R',0)))

        #  use negative page to prompt for talk or playlist search
        if page < 0:
            q = xbmcgui.Dialog().yesnocustom(
                self.ui.localized_string(30094), # search with topic
                self.ui.localized_string(30025) % (search_string),
                self.ui.localized_string(30023), # cancel
                self.ui.localized_string(30004), # search
                self.ui.localized_string(30005)) # search (playlist)
            if q < 0 or q > 1:
                xbmcplugin.endOfDirectory(__handle__)
                return
            cat= 'p' if bool(q) else 't'
            page = 1

        #  use zero page to always prompt for a search string
        if page < 1:
            label = self.ui.localized_string(30005 if cat == 'p' else 30004)
            keyboard = xbmc.Keyboard(settings.get_current_search(), label)
            keyboard.doModal()
            if not keyboard.isConfirmed():
                return
            search_string = keyboard.getText()
            settings.set_current_search(search_string)
            if not search_string:
                return
            page = 1

        #  no search_string, create new search or saved search actions
        if not search_string:
            self.ui.add_DirectoryItem(
                *self.create_search_action_listitem(0, cat))
            if bool(settings.get_current_search()):
                self.ui.add_DirectoryItem(
                    *self.create_search_action_listitem(1, cat))
            self.ui.end_Directory('videos', updateListing=False)
            return

        fetcher = self.ui.fetcher.get_HTML
        generator = Search(fetcher).fetch_search(search_string, page, cat)
        a, b, c = next(itertools.islice(generator, 1))
        action = 'playlist' if cat == 'p' else 'talkpage'
        for title, url, thumb, plot in generator:
            url = self.ui.create_action_url(action, url)
            li = self.ui.create_ListFldr(title, thumb, {
                'title': title, 'plot': plot, 'mediatype': 'video'})
            self.ui.add_DirectoryItem(url, li)
            a = a + 1
        if a < c:
            url = self.create_search_url(search_string, page+1, cat)
            li = self.ui.create_ListFldr(self.ui.localized_string(30022))
            li.setInfo('video', {'plot':' '})
            li.setProperty('SpecialSort', 'bottom')
            self.ui.add_DirectoryItem(url, li)
        self.ui.end_Directory('videos', updateListing=(page>1) or R)


class TopicsAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(TopicsAction, self).__init__('topics', [], *args, **kwargs)
        self.ui = ui

    def create_video_info(self, cat, data):
        def P(d):
            return {
                'title': '%s (%d talks) - Playlist' % (d['title'], d['count']),
                'originaltitle': d['title'],
                'plot': d['plot'],
                'tvshowtitle': d['title'],
                'totalepisodes': d['count'],
                'tag': d['tag'],
                'mediatype': d['mediatype']
            }
        def T(d):
            return {
                'title': '%s | %s' % (d['title'], d['author']),
                'originaltitle': d['title'],
                'plot': d['plot'],
                #'duration': int(d['duration']),
                'cast': [d['author']],
                'tag': d['tag'],
                'mediatype': d['mediatype']
            }
        return P(data) if cat == 'p' else T(data)

    def create_topic_listitem(self, topic, topic_slug):
        def S(id): return self.ui.localized_string(id)
        def search_with_topic():
            url = self.ui.create_action_url('search', '-1', {'q':topic})
            return 'ActivateWindow(Videos,%s,return)' % (url)
        icon = settings.__plugin_icon__
        url = self.ui.create_action_url('topics', topic_slug)
        li = self.ui.create_ListFldr(topic, icon, S(30037))
        li.addContextMenuItems([(S(30004), search_with_topic())])
        return (url, li, True)

    def run_internal(self, args):
        topic_slug = args.get('url','')
        topics = Topics(self.ui.fetcher.get_HTML)

        # list of topics
        if not bool(topic_slug):
            listitems = []
            for topic, slug in topics.fetch_topics():
                listitems += [self.create_topic_listitem(topic, slug)]
            self.ui.add_DirectoryItems(listitems)
            self.ui.end_Directory('files', ['title'])
            return

        # featured playlists and talks 
        for cat, data in topics.fetch_featured(topic_slug):
            action = 'playlist' if cat == 'p' else 'talkpage'
            url = self.ui.create_action_url(action, data['url'])
            vid = self.create_video_info(cat, data)
            li = self.ui.create_ListFldr(vid['title'], data['thumb'])
            li.setInfo('video', vid)
            self.ui.add_DirectoryItem(url, li)
        self.ui.end_Directory('videos', ['none', 'title'])


class SpeakersAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(SpeakersAction, self).__init__('people', [], *args, **kwargs)
        self.ui = ui
        self.ppg = 4  # pages per group
        self.label = self.ui.localized_string(30002)
        self.icon = settings.__speaker_icon__

    def create_action_url(self, url, R=False):
        R = {'R':'1'} if R else {}
        return self.ui.create_action_url('people', url, R)

    def create_groups_item(self, page):
        title = '%s...  %d' % (self.label, page // self.ppg +1)
        art = {'thumb': self.icon, 'poster': self.icon}
        return self.ui.create_ListFldr(title, art, ' ')

    def create_person_item(self, name, thumb, tagline, desc=None):
        def J(s): return s.join([name, tagline])
        li = self.ui.create_ListFldr(J(' | '),thumb, desc if desc else J('\n'))
        li.setCast([{'name': name, 'role': tagline, 'thumbnail': thumb}])
        return li

    def run_internal(self, args):
        url = args.get('url')
        R = bool(args.get('R'))

        speakers = Speakers(self.ui.fetcher.get_HTML)

        # intial speaker groups
        if not url:
            N = speakers.get_speaker_page_count()
            items = []
            for a in range(1, N+1, self.ppg):
                b = min(a + self.ppg -1, N)
                url = self.create_action_url('%s-%s' % (a, b))
                li = self.create_groups_item(a)
                items += [(url, li, True)]
            self.ui.add_DirectoryItems(items)
            self.ui.end_Directory('artists'),
            return

        # list of speakers
        if not url.startswith('http'):
            pages = url.split('-')
            pages = list(range(int(pages[0]), int(pages[1]) +1))
            generator = speakers.get_speakers_for_pages(pages)
            N = next(itertools.islice(generator, 1))
            items = []
            for name, url, thumb, tagline in generator:
                url = self.create_action_url(url)
                li = self.create_person_item(name, thumb, tagline)
                items += [(url, li, True)]
            self.ui.add_DirectoryItems(items)
            if pages[-1] < N:
                a = pages[-1] + 1
                b = min(N, pages[-1] + self.ppg)
                url = self.create_action_url('%s-%s' % (a, b), True)
                li = self.create_groups_item(a)
                li.setProperty('SpecialSort', 'bottom')
                self.ui.add_DirectoryItem(url, li)
            xbmcplugin.setPluginCategory(__handle__, self.label)
            self.ui.end_Directory('', updateListing=R)
            return

        # individual speaker page
        generator = speakers.get_talks_for_speaker(url)
        who, thumb, tagline, intro,extra = next(itertools.islice(generator, 1))
        url = self.create_action_url(url, True)
        li = self.create_person_item(who, thumb, tagline, {
            'title': ' | '.join([who, tagline]),
            'tagline': tagline,
            'plot': '\n\n'.join([intro, extra])
        })
        li.setProperty('SpecialSort', 'top')
        self.ui.add_DirectoryItem(url, li)
        for urlp, subp, vid, art, spkr in generator:
            url = self.ui.create_action_url('play_video', vid.get('url'))
            li = self.ui.create_ListItem(urlp, subp, vid, art, spkr)
            self.ui.add_DirectoryItem(url, li, False)
        self.ui.end_Directory('videos', ['title','date'], updateListing=R)


class SeriesAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(SeriesAction, self).__init__('series', [], *args, **kwargs)
        self.ui = ui

    def run_internal(self, args):
        url = args.get('url')
        md5 = args.get('md5', '')
        N = int(args.get('se', 0)) #season

        series = Series(self.ui.fetcher.get_HTML)

        # list of series
        if not bool(url):
            label = self.ui.localized_string(30008)
            for title, url, img, plot in series.fetch_list():
                li = self.ui.create_ListFldr('%s: %s' % (label, title), img)
                li.setInfo('video', {'plot': plot, 'mediatype': 'tvshow'})
                url = self.ui.create_action_url('series', url)
                self.ui.add_DirectoryItem(url, li)
            self.ui.end_Directory('tvshows', ['title'])
            return

        # seasons for a series
        if not bool(N):
            generator = series.fetch_series(url)
            common, md5 = next(itertools.islice(generator, 1))
            for se in generator:
                # the url is not reliable, use the series url instead
                url = self.ui.create_action_url('series', common['url'], {
                    'md5': md5, # hash for our cached file
                    'se': str(se['season'])
                })
                li = self.ui.create_ListFldr(se['title'], se['img'], {
                    'title': se['title'],
                    'tvshowtitle': common['title'],
                    'season': se['season'],
                    'plot': se['plot'],
                    'mediatype': se['mediatype']
                })
                self.ui.add_DirectoryItem(url, li)
            self.ui.end_Directory('seasons', ['episode'])
            return

        # episodes for a season
        generator = series.fetch_season(url, md5, N)
        common, a, b = next(itertools.islice(generator, 1))
        for urlp, subp, vid, art, spkr in generator:
            url = self.ui.create_action_url('play_video', vid.get('url'))
            li = self.ui.create_ListItem(urlp, subp, vid, art, spkr)
            self.ui.add_DirectoryItem(url, li, False)
        self.ui.end_Directory('episodes', ['episode', 'date'])


class RssFeedsAction(Action):

    def __init__(self, ui, *args, **kwargs):
        super(RssFeedsAction, self).__init__('rss', [], *args, **kwargs)
        self.ui = ui

    def talkpage_menu_item(self, url):
        return (self.ui.localized_string(30091),
                'ActivateWindow(Videos,%s,return)' % (
                    self.ui.create_action_url('talkpage', url)))

    def read_opml(self):
        try:
            with open(settings.__rssfeed_opml__, 'r') as fp:
                content = fp.read()
        except:
            return
        # #!# assumes a single line holds all of the info we need
        for s in content.split('\n'):
            if not (s.find('<outline ') < 0):
                m = re.search('xmlUrl="([^"]*)"', s)
                url = m.group(1) if m else ''
                m = re.search('text="([^"]*)"', s)
                title = m.group(1) if m else ''
                m = re.search('description="([^"]*)"', s)
                desc = m.group(1) if m else ''
                m = re.search('kodi:iconUrl="([^"]*)"', s)
                thumb = m.group(1) if m else ''
                yield url, title, thumb, desc

    def run_internal(self, args):
        url = args.get('url')

        # no url, so show the list of feeds
        if not url:
            for url, title, thumb, desc in self.read_opml():
                li = self.ui.create_ListFldr(title, thumb, desc)
                url = self.ui.create_action_url('rss', url)
                self.ui.add_DirectoryItem(url, li)
            self.ui.end_Directory()
            return

        # with url, fetch a specific feed
        feeds = NewTalksRss(logger)
        for talk in feeds.get_new_talks(url if url != 'latest' else None):
            media = talk.pop('media')
            art = talk.pop('thumb', '')
            art = { 'thumb': art }
            urlp = talk.get('url', '')
            url = self.ui.create_action_url('play_video', urlp)
            li = self.ui.create_ListItem(media, None, talk, art, None)
            li.addContextMenuItems([self.talkpage_menu_item(urlp)])
            self.ui.add_DirectoryItem(url, li, False)
        self.ui.end_Directory('videos', ['date', 'title'])


class Main:

    def __init__(self, args_map):
        self.args_map = args_map
        self.fetcher = Fetcher(logger)

    def run(self):
        ui = UI(self.fetcher)
        if 'mode' not in self.args_map:
            ui.showCategories()
        else:
            modes = [
                PlayVideoAction(ui),
                TalkPageAction(ui),
                PlaylistAction(ui),
                SearchAction(ui),
                TopicsAction(ui),
                SpeakersAction(ui),
                SeriesAction(ui),
                RssFeedsAction(ui)
            ]
            modes = dict([(m.mode, m) for m in modes])
            mode = self.args_map['mode']
            if mode in modes:
                modes[mode].run(self.args_map)
            else:
                # bit of a hack (cough)
                Action(mode, []).report_problem(self.args_map)
