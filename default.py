
import sys
import resources.lib.model.arguments as arguments
import resources.lib.ted_talks as ted_talks
import resources.lib.settings as settings

settings.initialize()

if __name__ == "__main__":
    args_map = arguments.parse_arguments(sys.argv[2])
    ted_talks.Main(args_map=args_map).run()
