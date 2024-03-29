plugin.video.ted.talks
===========================
This is a fork of the project started by rwparris, see
[here](http://forum.xbmc.org/showthread.php?tid=36866).

Fix for Kodi 19.x Matrix and Kodi 20.x Nexus implemented by [Kevwag-Kodi-Forks](https://githuc.com/Kevwag-Kodi-Forks)

For installation instructions see
[Installing](https://github.com/moreginger/xbmc-plugin.video.ted.talks/wiki/Installing)

The goal is (_surprise_) to allow watching TED talks in XBMC.
The currently supported browsing options are:
* Newest talks
* Search
* Speakers
* Topics

Playback uses an m3u8 playlist file. Kodi will automatically select the best
bitrate supported by the bandwidth settings of the installation.


Settings
========

![settings screen shot](README/settings.png)

__Enable subtitles__: Check this option to show subtitles.
By default the subtitles will be shown in the current XBMC language.

__Custom language code__: Set a custom language code (ISO639-1) if required.
It is also possible to enter a comma separated list of language codes (e.g. _pt-br,pt,en_)
which will show subtitles in the first language which matches.


Known issues
============

Plugin will fail with certain versions of pyOpenSSL, see
https://github.com/jdf76/plugin.video.youtube/issues/14


Bugs
====
Bugs and enhancement suggestions can be reported
[here](https://github.com/moreginger/xbmc-plugin.video.ted.talks/issues).
