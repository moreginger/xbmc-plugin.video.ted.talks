"""
    TED Talks
    rwparris2
"""
import sys
import resources.lib.plugin as plugin

if __name__ == "__main__":
    plugin.init()
    import resources.lib.ted_talks as ted_talks
    action = sys.argv[2]
    if not action:
        action = ""

    if action.startswith('?addToFavorites'):
        ted_talks.Main(logger = plugin.log, checkMode = False).addToFavorites(action.split('=')[-1])
    elif action.startswith('?removeFromFavorites'):
        ted_talks.Main(logger = plugin.log, checkMode = False).removeFromFavorites(action.split('=')[-1])
    elif action.startswith('?downloadVideo'):
        ted_talks.Main(logger = plugin.log, checkMode = False).downloadVid(action.split('=')[-1])
    else:
        ted_talks.Main(logger = plugin.log, checkMode = True)

sys.modules.clear()
