import urllib

def parse_arguments(custom_args):
    args_map = {}
    if custom_args:
        args = custom_args[1:].split('&')
        for arg in args:
            if len(arg) > 0:
                split = arg.partition('=')
                args_map[split[0]] = urllib.unquote_plus(split[2])
    return args_map