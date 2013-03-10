from BeautifulSoup import MinimalSoup
import re

class Talk:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get(self, url):
        html = self.get_HTML(url)
        url = ""
        soup = MinimalSoup(html)
        # get title
        title = soup.find('span', attrs={'id':'altHeadline'}).string
        # get speaker from title
        speaker = title.split(':', 1)[0]
        # get description:
        plot = soup.find('p', attrs={'id':'tagline'}).string
        # get url
        # detectors for link to video in order of preference
        linkDetectors = [
            lambda l: re.compile('High-res video \(MP4\)').match(str(l.string)),
            lambda l: re.compile('http://download.ted.com/talks/.+.mp4').match(str(l['href'])),
        ]
        for link in soup.findAll('a', href=True):
            for detector in linkDetectors:
                if detector(link):
                    url = link['href']
                    linkDetectors = linkDetectors[:linkDetectors.index(detector)]  # Only look for better matches than what we have
                    break

        if url == "":
            # look for utub link
            utublinks = re.compile('http://(?:www.)?youtube.com/v/([^\&]*)\&').findall(html)
            for link in utublinks:
                url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (link)

        return url, title, speaker, plot
