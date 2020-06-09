from getopt import getopt, GetoptError
import sys
import os

if __name__ == "__main__":
    usage = "Usage: python -m modi -options" \
                "\n\nOptions:\n-h, --tutorial: Interactive Tutorial"

    try:
        opts, args = getopt(sys.argv[1:], 'hdn:u',
                            ["tutorial", "debug", "nb_modules=", "update"])
    except GetoptError as err:
        print(str(err))
        print(usage)
        os._exit(2)

    if len(args) > 0 or len(sys.argv) == 1:
        print(usage)
        os._exit(2)

    for o, a in opts:
        if o in ('-h', '--tutorial'):
            from modi.util.tutorial import tutorial
            tutorial()
            os._exit(0)
        if o in ('-d', '--debug'):
            print(opts[:, 0])
