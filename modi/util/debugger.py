import sys
import os
import modi
from getopt import getopt, GetoptError
import time

if __name__ == '__main__':
    usage = "Usage: python -i modi_debugger.py -n <nb_modules>" \
            "\n\nOptions:\n-h, --help: Print help message" \
            "\n-n, --nb_modules: specify number of modules" \
            "\n-u, --update: update the modules"

    try:
        opts, args = getopt(sys.argv[1:], 'hn:u',
                            ["help", "nb_modules=", "update"])
    except GetoptError as err:
        print(str(err))
        print(usage)
        os._exit(2)

    if len(args) > 0 or len(sys.argv) == 1:
        print(usage)
        os._exit(2)

    is_update = False

    for o, a in opts:
        if o in ('-n', '--nb_modules'):
            nb_modules = int(a)
        elif o in ('-h', '--help'):
            print(usage)
            os._exit(0)
        if o in ('-u', '--update'):
            is_update = True

    print(">>> bundle = modi.MODI(" + str(nb_modules) + ")")
    init_time = time.time()
    bundle = modi.MODI(nb_modules)
    fin_time = time.time()

    print(f'Took {fin_time - init_time} seconds to finish the job')

    print(">>>")

    for module in bundle.modules:
        module_name = type(module).__name__.lower()
        print(">>> " + module_name + " = bundle." + module_name + "s[0]")
        exec(module_name + " = module")

    print(">>>")

    if is_update:
        print(">>> bundle.update_module_firmware()")
        bundle.update_module_firmware()
