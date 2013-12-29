"""
Contains constants that we initialize to the correct values at runtime.
Should be usable as a testing shim.
"""
import model.language_mapping as language_mapping

__plugin_id__ = 'plugin.video.ted.talks'
__previous_search__ = 'previous_search'

username = 'Ted'
password = 'Ted'
download_mode = True
download_path = '/tmp/'
video_quality = 3
enable_subtitles = True
xbmc_language = 'English'
subtitle_language = 'en'
previous_search = ''

def init():
    import xbmc, xbmcaddon
    addon = xbmcaddon.Addon(id=__plugin_id__)
    global username, password, download_mode, download_path, video_quality, enable_subtitles, xbmc_language, subtitle_language, previous_search
    username = addon.getSetting('username')
    password = addon.getSetting('password')
    download_mode = addon.getSetting('downloadMode')
    download_path = addon.getSetting('downloadPath')
    video_quality = addon.getSetting('video_quality')
    enable_subtitles = addon.getSetting('enable_subtitles')
    xbmc_language = xbmc.getLanguage()
    subtitle_language = addon.getSetting('subtitle_language')
    previous_search = __get_cache__().get(__previous_search__)
    
def __get_cache__():
    import StorageServer
    return StorageServer.StorageServer('xbmc-plugin.video.ted.talks', 24 * 7 * 2) # 2 weeks of storage. Who cares after that long? 

def get_subtitle_languages():
    '''
    Returns list of ISO639-1 language codes in order of preference,
    or None if disabled.
    '''
    if enable_subtitles == 'false':
        return None
    if not subtitle_language.strip():
        code = language_mapping.get_language_code(xbmc_language)
        return [code] if code else None
    else:
        return [code.strip() for code in subtitle_language.split(',') if code.strip()]

def set_previous_search(value):
    __get_cache__().set(__previous_search__, value)
