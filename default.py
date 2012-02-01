"""
    TED Talks
    rwparris2
"""
import sys
import resources.lib.plugin as plugin

if __name__ == "__main__":
    plugin.init()
    import resources.lib.ted_talks as ted_talks
    if not sys.argv[2]:
        ted_talks.Main()
    elif sys.argv[2].startswith('?addToFavorites'):
        ted_talks.Main(checkMode=False).addToFavorites(sys.argv[2].split('=')[-1])
    elif sys.argv[2].startswith('?removeFromFavorites'):
        ted_talks.Main(checkMode=False).removeFromFavorites(sys.argv[2].split('=')[-1])
    elif sys.argv[2].startswith('?downloadVideo'):
        ted_talks.Main(checkMode=False).downloadVid(sys.argv[2].split('=')[-1])
    else:
        ted_talks.Main()

sys.modules.clear()
