"""
Contains constants that we initialize to the correct values at runtime.
"""
username = 'Ted'
password = 'Ted'
download_mode = True
download_path = '/tmp/'


def init():
    import xbmcaddon
    addon = xbmcaddon.Addon(id='plugin.video.ted.talks')
    global username, password, download_mode, download_path
    username = addon.getSetting('username')
    password = addon.getSetting('password')
    download_mode = addon.getSetting('downloadMode')
    download_path = addon.getSetting('downloadPath')
