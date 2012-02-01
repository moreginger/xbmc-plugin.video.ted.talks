__plugin__ = "TED Talks Dev Build"
__author__ = "XXX"
__version__ = "X.X.X"


def init():
    import sys
    main = sys.modules['__main__']
    global __plugin__, __author__, __version__
    __plugin__ = main.__plugin__
    __author__ = main.__author__
    __version__ = main.__version__
    print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)
