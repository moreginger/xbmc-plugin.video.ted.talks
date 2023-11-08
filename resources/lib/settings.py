"""
Contains constants that we initialize to the correct values at runtime.
Should be usable as a testing shim.
"""
import os

__ted_url__ = 'https://www.ted.com'
__plugin_id__ = 'plugin.video.ted.talks'

__plugin_icon__ = None
__speaker_icon__ = None
__rssfeed_opml__ = None

__saved_search_path__ = None
__subtitle_languages__ = None

__get_localized_string__ = lambda x: x

def get_localized_string(id):
    return __get_localized_string__(id)

def get_subtitle_languages():
    return __subtitle_languages__

def set_current_search(value):
    with open(__saved_search_path__, 'w') as fp:
        fp.write(value)

def get_current_search():
    if os.path.exists(__saved_search_path__):
        with open(__saved_search_path__, 'r') as fp:
            return fp.read()
    return ''

def report(gnarly_message, friendly_message=None, level='info'):
    '''
    Log a message with optional onscreen notification.
    '''
    import xbmc
    import xbmcaddon

    level = {
        'info' : xbmc.LOGINFO,
        'warn' : xbmc.LOGWARNING,
        'debug': xbmc.LOGDEBUG
    }.get(level, 'info')

    addon = xbmcaddon.Addon(id=__plugin_id__)

    p = addon.getAddonInfo('name')
    v = addon.getAddonInfo('version')
    xbmc.log("[ADDON] %s v%s - %s" % (p, v, gnarly_message), level=level)

    if friendly_message:
        p = addon.getLocalizedString(30000)
        xbmc.executebuiltin('Notification("%s","%s",)' % (p, friendly_message))


def initialize():

    import xbmc
    import xbmcvfs
    import xbmcaddon

    global __plugin_icon__
    global __speaker_icon__
    global __rssfeed_opml__
    global __saved_search_path__
    global __subtitle_languages__
    global __get_localized_string__

    def get_subtitle_languages(addon):
        '''
        Returns list of ISO639-1 language codes in order of preference,
        or None if disabled.
        '''
        if addon.getSetting('enable_subtitles') == 'false':
            return None
        sl = addon.getSetting('subtitle_language').strip()
        if not sl:
            return [xbmc.getLanguage(xbmc.ISO_639_1)]
        return [x.strip() for x in sl.split(',') if x.strip()]

    addon = xbmcaddon.Addon(id=__plugin_id__)
    __get_localized_string__ = addon.getLocalizedString
    __subtitle_languages__ = get_subtitle_languages(addon)


    ppath = xbmcvfs.translatePath(addon.getAddonInfo('path'))
    ppath = os.path.join(ppath, 'resources')
    __speaker_icon__ = os.path.join(ppath, 'speaker.png')
    __rssfeed_opml__ = os.path.join(ppath, 'rss_feeds.opml')
    __plugin_icon__ = xbmcvfs.translatePath(addon.getAddonInfo('icon'))

    ppath = xbmcvfs.translatePath(addon.getAddonInfo('profile'))
    if not os.path.exists(ppath):
        os.makedirs(ppath)
    __saved_search_path__ = os.path.join(ppath, 'TED_search_string')

    #report('INITIALIZED')
