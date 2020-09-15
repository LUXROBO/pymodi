import os
import sys
import time
import textwrap

from getopt import getopt, GetoptError

import modi

from modi.debugger import Debugger
from modi.util.tutor import Tutor
from modi.util.inspector import Inspector

from modi.firmware_updater import STM32FirmwareUpdater
from modi.firmware_updater import ESP32FirmwareUpdater
from modi.util.msgutil import parse_message, decode_message


def check_option(*options):
    for o, a in opts:
        if o in options:
            return a if a else True
    return False


if __name__ == "__main__":
    usage = textwrap.dedent(
        """
        Usage: python -m modi -<options>
        Options:
        -t, --tutorial: Interactive Tutorial
        -d, --debug: Auto initialization debugging mode
        -h, --help: Print out help page
        """.rstrip()
    )

    help_page = textwrap.dedent(
        """
        Usage: python -m modi -<options>
        Options:
        -t, --tutorial: Interactive Tutorial
             Usage: python -m modi --tutorial
        -d, --debug: Auto initialize debugging mode
             Usage: python -m modi --debug -n <nb_modules>
        """.rstrip()
    )

    try:
        # all commands should be defined here in advance
        opts, args = getopt(
            sys.argv[1:], 'tdmhvpgin',
            [
                "tutorial",
                "debug",
                "update_module",
                "help",
                "verbose",
                "performance",
                "gui",
                "inspect",
                "update_network_module",
            ]
        )
    # exit program if an invalid option has been entered
    except GetoptError as err:
        print(str(err))
        print(usage)
        os._exit(2)

    # Ensure that there is an option but argument
    if len(sys.argv) == 1 or len(args) > 0:
        print(usage)
        os._exit(2)

    # Print help page
    if check_option('-h', '--help'):
        print(help_page)
        os._exit(0)

    # Start interactive pymodi tutorial
    if check_option('-t', '--tutorial'):
        pymodi_tutor = Tutor()
        pymodi_tutor.run_introduction()
        os._exit(0)

    # Time message transfer between local machine and network module
    if check_option('-p', '--performance'):
        print("[PyMODI Performance Test]" + "\n" + "=" * 25)
        init_time = time.time()
        bundle = modi.MODI()
        fin_time = time.time()
        took = (fin_time - init_time) * 100 // 1 / 100
        print("Hard waiting for topology data to be initialized...")
        time.sleep(0.5 * len(bundle.modules))
        bundle.print_topology_map(True)
        print(f"Took {took} seconds to initialize")
        req_tp_msg = parse_message(0x2A, 0, bundle.networks[0].id)
        print(f"sending request message... {req_tp_msg}")
        bundle._exe_thrd.close()
        init_time = time.perf_counter()
        bundle.send(req_tp_msg)
        msg = None
        while True:
            msg = bundle.recv()
            if not msg:
                continue
            recv_cmd = decode_message(msg)[0]
            if recv_cmd == 0x07:
                break
        fin_time = time.perf_counter()
        took = fin_time - init_time
        print(f"received message... {msg}")
        print(f"Took {took / 2:.10f} seconds for message transfer")
        os._exit(0)

    # Update STM32 modules (every modules but network module)
    if check_option('-m', '--update_module'):
        init_time = time.time()
        updater = STM32FirmwareUpdater()
        updater.update_module_firmware()
        fin_time = time.time()
        print(f"Took {fin_time - init_time:.2f} seconds to update")
        os._exit(0)

    # Update ESP32 module (only network module)
    if check_option('-n', '--update_network_module'):
        init_time = time.time()
        updater = ESP32FirmwareUpdater()
        updater.update_firmware()
        fin_time = time.time()
        print(f"Took {fin_time - init_time:.2f} seconds to update")
        os._exit(0)

    # Initialize modules implicitly
    if check_option('-d', '--debug'):
        # TODO: Handle when there are more than one module with the same type
        print(">>> bundle = modi.MODI()")
        init_time = time.time()
        bundle = modi.MODI(verbose=check_option('-v', '--verbose'))
        fin_time = time.time()
        print(f'Took {fin_time - init_time:.2f} seconds to init MODI modules')

        for module in bundle.modules:
            module_name = module.module_type.lower()
            print(">>> " + module_name + " = bundle." + module_name + "s[0]")
            exec(module_name + " = module")

    # Run GUI debugger
    if check_option('-g', '--gui'):
        print(">>> bundle = modi.MODI()")
        init_time = time.time()
        bundle = Debugger()
        fin_time = time.time()
        print(f'Took {fin_time - init_time:.2f} seconds to init MODI modules')
        for module in bundle.modules:
            module_name = module.module_type.lower()
            print(">>> " + module_name + " = bundle." + module_name + "s[0]")
            exec(module_name + " = module")

    # Run inspection mode
    if check_option('-i', '--inspect'):
        print("inspection mode has not been implemented yet!")
        pymodi_inspector = Inspector()
        pymodi_inspector.run_inspection()
        os._exit(0)
