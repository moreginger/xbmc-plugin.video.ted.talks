from url_constants import URLSPEAKERS
from BeautifulSoup import SoupStrainer, MinimalSoup
import re


class Speakers:

    def __init__(self, get_HTML):
        self.get_HTML = get_HTML

    def get_speakers_for_letter(self, char):
        page_index = 1
        html = self.get_HTML(URLSPEAKERS % (page_index, char))
        while True:
            containers = SoupStrainer(name='a', attrs={'href':re.compile('/speakers/.+\.html')})
            found_speaker = False
            for speaker in MinimalSoup(html, parseOnlyThese=containers):
                if speaker.img:
                    found_speaker = True
                    title = speaker.img['alt']
                    link = speaker['href']
                    img = speaker.img['src']
                    yield title, link, img

            if found_speaker:
                page_index += 1
                html = self.get_HTML(URLSPEAKERS % (page_index, char))
            else:
                break
