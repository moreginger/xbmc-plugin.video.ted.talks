import unittest
import urllib.request, urllib.error, urllib.parse

from mock import MagicMock

from .model.test_util import CachedHTMLProvider
from . import ted_talks_scraper


class TestTedTalks(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock()
        self.sut = ted_talks_scraper.TedTalks(CachedHTMLProvider(), self.logger)

    def test_smoke_relative_path(self):
        '''
        m3u8 stream urls do not start with '/'. Should be resolved vs the m3u8 playlist URL.
        '''
        playlist, title, subs, info = self.sut.get_video_details('https://www.ted.com/talks/ariel_garten_know_thyself_with_a_brain_scanner.html')

        self.assertEqual('{}\n'.format('''
#EXTM3U
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-VERSION:4
#EXT-X-MEDIA:URI="https://hls.ted.com/project_masters/1580/index-f5-a1.m3u8?intro_master_id=2346",TYPE=AUDIO,GROUP-ID="audio0",LANGUAGE="en",NAME="low",DEFAULT=NO,AUTOSELECT=NO,CHANNELS="1"
#EXT-X-MEDIA:URI="https://hls.ted.com/project_masters/1580/index-f8-a1.m3u8?intro_master_id=2346",TYPE=AUDIO,GROUP-ID="audio0",LANGUAGE="en",NAME="medium",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2"
#EXT-X-MEDIA:URI="https://hls.ted.com/project_masters/1580/index-f12-a1.m3u8?intro_master_id=2346",TYPE=AUDIO,GROUP-ID="audio0",LANGUAGE="en",NAME="high",DEFAULT=NO,AUTOSELECT=NO,CHANNELS="2"
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1231593,AVERAGE-BANDWIDTH=1094793,RESOLUTION=854x480,FRAME-RATE=59.92,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f9-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=163328,AVERAGE-BANDWIDTH=148605,RESOLUTION=320x180,FRAME-RATE=59.92,CODECS="avc1.42c00d,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f1-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=241739,AVERAGE-BANDWIDTH=216837,RESOLUTION=320x180,FRAME-RATE=59.92,CODECS="avc1.42c01e,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f2-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=371097,AVERAGE-BANDWIDTH=331981,RESOLUTION=416x234,FRAME-RATE=59.92,CODECS="avc1.42c01e,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f3-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=511004,AVERAGE-BANDWIDTH=460493,RESOLUTION=416x234,FRAME-RATE=59.92,CODECS="avc1.64001e,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f4-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=683948,AVERAGE-BANDWIDTH=598503,RESOLUTION=480x270,FRAME-RATE=59.92,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f6-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1019879,AVERAGE-BANDWIDTH=906897,RESOLUTION=640x360,FRAME-RATE=59.92,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f7-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1796457,AVERAGE-BANDWIDTH=1499914,RESOLUTION=1280x720,FRAME-RATE=59.92,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f10-v1.m3u8?intro_master_id=2346
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2825086,AVERAGE-BANDWIDTH=2537141,RESOLUTION=1280x720,FRAME-RATE=59.92,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/1580/index-f11-v1.m3u8?intro_master_id=2346
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=5227,RESOLUTION=320x180,CODECS="avc1.42c00d",URI="https://hls.ted.com/project_masters/1580/iframes-f1-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=12390,RESOLUTION=320x180,CODECS="avc1.42c01e",URI="https://hls.ted.com/project_masters/1580/iframes-f2-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=12396,RESOLUTION=416x234,CODECS="avc1.42c01e",URI="https://hls.ted.com/project_masters/1580/iframes-f3-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=30011,RESOLUTION=416x234,CODECS="avc1.64001e",URI="https://hls.ted.com/project_masters/1580/iframes-f4-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=25516,RESOLUTION=480x270,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/1580/iframes-f6-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=51839,RESOLUTION=640x360,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/1580/iframes-f7-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=55803,RESOLUTION=854x480,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/1580/iframes-f9-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=75088,RESOLUTION=1280x720,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/1580/iframes-f10-v1.m3u8?intro_master_id=2346"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=131800,RESOLUTION=1280x720,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/1580/iframes-f11-v1.m3u8?intro_master_id=2346"
'''.strip()), playlist)

    def test_smoke_full_path(self):
        '''
        m3u8 stream urls do not start with '/'. Should be resolved vs the domain of the m3u8 playlist URL.
        '''
        playlist, title, subs, info = self.sut.get_video_details('https://www.ted.com/talks/michael_levin_the_electrical_blueprints_that_orchestrate_life')

        self.assertEqual('{}\n'.format('''
#EXTM3U
#EXT-X-VERSION:4
#EXT-X-MEDIA:URI="https://hls.ted.com/videos/MichaelLevin_2020/audio/600k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a",TYPE=AUDIO,GROUP-ID="600k",LANGUAGE="en",NAME="Audio",DEFAULT=YES,AUTOSELECT=YES
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1919626,RESOLUTION=640x360,CODECS="avc1.42c01e,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/600k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=165255,RESOLUTION=320x180,CODECS="avc1.42c00c,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/64k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=461789,RESOLUTION=512x288,CODECS="avc1.42c015,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/180k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1054935,RESOLUTION=512x288,CODECS="avc1.42c015,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/320k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1474025,RESOLUTION=512x288,CODECS="avc1.42c015,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/450k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2866251,RESOLUTION=853x480,CODECS="avc1.4d401f,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/950k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3927925,RESOLUTION=1280x720,CODECS="avc1.640028,mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/video/1500k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=68059,CODECS="mp4a.40.2",AUDIO="600k"
https://hls.ted.com/videos/MichaelLevin_2020/audio/600k.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=49101,RESOLUTION=320x180,CODECS="avc1.42c00c",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/64k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=115454,RESOLUTION=512x288,CODECS="avc1.42c015",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/180k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=149958,RESOLUTION=512x288,CODECS="avc1.42c015",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/320k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=172518,RESOLUTION=512x288,CODECS="avc1.42c015",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/450k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=230908,RESOLUTION=640x360,CODECS="avc1.42c01e",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/600k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=370249,RESOLUTION=853x480,CODECS="avc1.4d401f",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/950k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
#EXT-X-I-FRAME-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=557365,RESOLUTION=1280x720,CODECS="avc1.640028",URI="https://hls.ted.com/videos/MichaelLevin_2020/video/1500k_iframe.m3u8?preroll=newshortintro_053119&uniqueId=b58e8c1a"
'''.strip()), playlist)