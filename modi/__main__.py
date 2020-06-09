from getopt import getopt, GetoptError
import sys
import os
import time
import modi


def check_option(*options):
    for o, a in opts:
        if o in options:
            return a if a else True
    return False


if __name__ == "__main__":
    usage = "Usage: python -m modi -<options>" \
            "\nOptions:\n-t, --tutorial: Interactive Tutorial" \
            "\n-d, --debug: Auto initialization debugging mode" \
            "\n-h, --help: Print out help page"

    help_page = "Usage: python -m modi -<options>" \
                "\n\nOptions:" \
                "\n-t, --tutorial: Interactive Tutorial" \
                "\n     Usage: python -m modi --tutorial" \
                "\n-d, --debug: Auto initialize debugging mode" \
                "\n     Usage: python -m modi --debug -n <nb_modules>" \
                "\n     options: -u, --update: update the module firmware" \
                "\n              -n, --nb_moodules: number of modules" \
                " connected to the network module" \
                "\n     If you want to use debugger in an interactive shell," \
                " use: python -im modi -n <nb_modules> -<options>"

    try:
        opts, args = getopt(sys.argv[1:], 'tdn:uh',
                            ["tutorial", "debug", "nb_modules=", "update",
                             "help"])
    except GetoptError as err:
        print(str(err))
        print(usage)
        os._exit(2)

    if len(args) > 0 or len(sys.argv) == 1:
        print(usage)
        os._exit(2)

    if check_option('-h', '--help'):
        print(help_page)
        os._exit(0)

    if check_option('-t', '--tutorial'):
        from modi.util.tutor import Tutor
        modi_tutor = Tutor()
        modi_tutor.start()
        os._exit(0)

    if check_option('-d', '--debug'):
        nb_modules = check_option('-n', '--nb_modules')
        if not nb_modules:
            print("Please provide number of modules")
            print(usage)
            os._exit(2)
        is_update = check_option('-u', '--update')
        nb_modules = int(nb_modules)
        print(">>> bundle = modi.MODI(" + str(nb_modules) + ")")
        init_time = time.time()
        bundle = modi.MODI(nb_modules)
        fin_time = time.time()

        print(f'Took {fin_time - init_time:.2f} seconds to finish the job')

        print(">>>")

        for module in bundle.modules:
            module_name = type(module).__name__.lower()
            print(">>> " + module_name + " = bundle." + module_name + "s[0]")
            exec(module_name + " = module")

        print(">>>")

        if is_update:
            print(">>> bundle.update_module_firmware()")
            bundle.update_module_firmware()
