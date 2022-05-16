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
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-VERSION:4
#EXT-X-MEDIA:URI="https://hls.ted.com/project_masters/7135/index-f5-a1.m3u8",TYPE=AUDIO,GROUP-ID="audio0",LANGUAGE="en",NAME="low",DEFAULT=NO,AUTOSELECT=NO,CHANNELS="1"
#EXT-X-MEDIA:URI="https://hls.ted.com/project_masters/7135/index-f8-a1.m3u8",TYPE=AUDIO,GROUP-ID="audio0",LANGUAGE="en",NAME="medium",DEFAULT=YES,AUTOSELECT=YES,CHANNELS="2"
#EXT-X-MEDIA:URI="https://hls.ted.com/project_masters/7135/index-f12-a1.m3u8",TYPE=AUDIO,GROUP-ID="audio0",LANGUAGE="en",NAME="high",DEFAULT=NO,AUTOSELECT=NO,CHANNELS="2"
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1081281,AVERAGE-BANDWIDTH=829523,RESOLUTION=854x480,FRAME-RATE=29.97,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f9-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=145745,AVERAGE-BANDWIDTH=108690,RESOLUTION=320x180,FRAME-RATE=29.97,CODECS="avc1.42c00d,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f1-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=238723,AVERAGE-BANDWIDTH=210503,RESOLUTION=320x180,FRAME-RATE=29.97,CODECS="avc1.42c01e,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f2-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=323860,AVERAGE-BANDWIDTH=236167,RESOLUTION=416x234,FRAME-RATE=29.97,CODECS="avc1.42c01e,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f3-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=442204,AVERAGE-BANDWIDTH=357755,RESOLUTION=416x234,FRAME-RATE=29.97,CODECS="avc1.64001e,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f4-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=527501,AVERAGE-BANDWIDTH=399562,RESOLUTION=480x270,FRAME-RATE=29.97,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f6-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=883792,AVERAGE-BANDWIDTH=689311,RESOLUTION=640x360,FRAME-RATE=29.97,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f7-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=1734352,AVERAGE-BANDWIDTH=1305092,RESOLUTION=1280x720,FRAME-RATE=29.97,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f10-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2829500,AVERAGE-BANDWIDTH=2140552,RESOLUTION=1280x720,FRAME-RATE=29.97,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f11-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3781469,AVERAGE-BANDWIDTH=3020243,RESOLUTION=1920x1080,FRAME-RATE=29.97,CODECS="avc1.640029,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f13-v1.m3u8
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=4333586,AVERAGE-BANDWIDTH=3228925,RESOLUTION=1920x1080,FRAME-RATE=29.97,CODECS="avc1.640029,mp4a.40.2",AUDIO="audio0"
https://hls.ted.com/project_masters/7135/index-f14-v1.m3u8
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=3974,RESOLUTION=320x180,CODECS="avc1.42c00d",URI="https://hls.ted.com/project_masters/7135/iframes-f1-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=12266,RESOLUTION=320x180,CODECS="avc1.42c01e",URI="https://hls.ted.com/project_masters/7135/iframes-f2-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=9023,RESOLUTION=416x234,CODECS="avc1.42c01e",URI="https://hls.ted.com/project_masters/7135/iframes-f3-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=28807,RESOLUTION=416x234,CODECS="avc1.64001e",URI="https://hls.ted.com/project_masters/7135/iframes-f4-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=28498,RESOLUTION=480x270,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/7135/iframes-f6-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=48178,RESOLUTION=640x360,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/7135/iframes-f7-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=56648,RESOLUTION=854x480,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/7135/iframes-f9-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=79166,RESOLUTION=1280x720,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/7135/iframes-f10-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=134485,RESOLUTION=1280x720,CODECS="avc1.64001f",URI="https://hls.ted.com/project_masters/7135/iframes-f11-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=193483,RESOLUTION=1920x1080,CODECS="avc1.640029",URI="https://hls.ted.com/project_masters/7135/iframes-f13-v1.m3u8"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=206578,RESOLUTION=1920x1080,CODECS="avc1.640029",URI="https://hls.ted.com/project_masters/7135/iframes-f14-v1.m3u8"
'''.strip()), playlist)