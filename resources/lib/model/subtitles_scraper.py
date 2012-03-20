'''
Inspired by code of Esteban Ordano

http://estebanordano.com/ted-talks-download-subtitles/
http://estebanordano.com.ar/wp-content/uploads/2010/01/TEDTalkSubtitles.py_.zip
'''
import simplejson
import urllib
import sys
import re

def format_time(time):
    millis = time % 1000
    seconds = (time / 1000) % 60
    minutes = (time / 60000) % 60
    hours = (time / 3600000)
    return "%02d:%02d:%02d,%03d" % (hours, minutes, seconds, millis)

def get_languages(soup):
    languages = soup.find('select', attrs = {'id': 'languageCode'}).findAll('option')
    return [l['value'].encode('ascii') for l in languages]

