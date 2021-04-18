import requests

class Fetcher:

    def __init__(self, logger):
        self.logger = logger

    def get_HTML(self, url, data=None):
        self.logger('GET {}'.format(url))

        r = requests.get(url)
        if r.ok:
            return r.text
        else:
            self.logger('%s\n%s\n%s'.format(r.status_code, r.headers, r.text))
            raise Exception('Failed to GET {}: {}'.format(url, r.status_code))
