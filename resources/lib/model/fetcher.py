import CommonFunctions as xbmc_common

class Fetcher:

    def __init__(self, logger):
        self.logger = logger

    def getHTML(self, url, data=None):
        """
        url Might be a real URL object or a String-like thing.
        """
        try:
            url = url.get_full_url()
        except AttributeError:
            pass
        self.logger('%s attempting to open %s with data' % (__name__, url))

        result = xbmc_common.fetchPage({'link': url})
        if result["status"] == 200:
            return result["content"]
        else:
            self.logger('%s error:\n%s\n%s\n%s' % (__name__, result['status'], result['header'], result['content']))
            raise Exception('Failed to fetch url "%s": %s' % (url, result['status']))
