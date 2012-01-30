import urllib2
import cookielib
import os.path
import xbmc
import sys

pluginName = sys.modules['__main__'].__plugin__

class Fetcher:

    def getHTML(url, cookiefile = xbmc.translatePath('special://temp/ted-cookies.lwp'), headers = [('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')]):
        """Returns HTML from a given URL"""
        try:
            print '[%s] %s attempting to open %s with data' % (pluginName, __name__, url.get_full_url())
        except:
            print '[%s] %s attempting to open %s' % (pluginName, __name__, url)
        #create cookiejar
        cj = cookielib.LWPCookieJar()
        #load any existing cookies
        if os.path.isfile(cookiefile):
            cj.load(cookiefile)
            #log what cookies were loaded
            for index, cookie in enumerate(cj):
                print '[%s] loaded cookie : %s\nfrom %s' % (pluginName, cookie, cookiefile)
        #build opener with automagic cookie handling abilities.
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = headers
        try:
            usock = opener.open(url)
            response = usock.read()
            usock.close()
            cj.save(cookiefile)
            return response
        except urllib2.HTTPError, error:
            print '[%s] %s error:\n%s\n%s\n%s' % (pluginName, __name__, error.code, error.msg, error.geturl())
        except Exception, error:
            print Exception.__module__
            print dir(error)
