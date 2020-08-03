import os
import sys
import time
from getopt import getopt, GetoptError

import modi
from modi.util.tutor import Tutor
from modi.firmware_updater import STM32FirmwareUpdater
from modi.util.msgutil import parse_message, decode_message


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
        opts, args = getopt(sys.argv[1:], 'tdn:uhvp',
                            ["tutorial", "debug", "nb_modules=", "update",
                             "help", "verbose", "performance"])
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
        modi_tutor = Tutor()
        modi_tutor.start()
        os._exit(0)

    if check_option('-p', '--performance'):
        print("[PyMODI Performance Test]" + "\n" + "=" * 25)
        init_time = time.time()
        bundle = modi.MODI()
        fin_time = time.time()
        took = (fin_time - init_time) * 100 // 1 / 100
        bundle.print_topology_map(True)
        print(f"Took {took} seconds to initialize")
        time.sleep(1)
        msg = parse_message(0x03, 0, bundle.modules[0].id, (1, None, 96, None))
        print(f"sending request message... {msg}")
        init_time = time.time()
        bundle.send(msg)
        while True:
            msg = bundle.recv()
            if msg and decode_message(msg)[0] == 0x1F:
                break
        fin_time = time.time()
        took = round((fin_time - init_time) / 2, 2)
        print(f"received message... {msg}")
        print(f"Took {took} seconds for message transfer")
        exit(0)

    if check_option('-u', '--update'):
        init_time = time.time()
        updater = STM32FirmwareUpdater()
        updater.update_module_firmware()
        fin_time = time.time()
        print(f"Took {fin_time - init_time:.2f} seconds to update")
        exit(0)

    if check_option('-d', '--debug'):
        nb_modules = check_option('-n', '--nb_modules')
        is_update = check_option('-u', '--update')
        nb_modules = int(nb_modules)
        print(">>> bundle = modi.MODI(" + str(nb_modules) + ")")
        init_time = time.time()
        if nb_modules:
            bundle = modi.MODI(nb_modules, verbose=check_option('-v',
                                                                '--verbose'))
        else:
            bundle = modi.MODI(verbose=check_option('-v', '--verbose'))
        fin_time = time.time()

        print(f'Took {fin_time - init_time:.2f} seconds to finish the job')

        print(">>>")

        for module in bundle.modules:
            module_name = type(module).__name__.lower()
            print(">>> " + module_name + " = bundle." + module_name + "s[0]")
            init_time = time.time()
            exec(module_name + " = module")
            fin_time = time.time()
            print(f'Took {fin_time - init_time:.2f} seconds '
                  f'to get {module_name}')
        print(">>>")
