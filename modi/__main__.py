import os
import sys
import time
import textwrap

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
             If you want to use debugger in an interactive shell, use: python -im modi -d
        """.rstrip()
    )

    try:
        opts, args = getopt(
            sys.argv[1:], 'tduhvpg',
            ["tutorial", "debug", "update", "help", "verbose", "performance", "gui"]
        )
    except GetoptError as err:
        print(str(err))
        print(usage)
        os._exit(2)

    if len(args) > 0 or len(sys.argv) == 1:
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

    # Time message transfer to check performance
    if check_option('-p', '--performance'):
        print("[PyMODI Performance Test]" + "\n" + "=" * 25)
        init_time = time.time()
        bundle = modi.MODI()
        fin_time = time.time()
        took = (fin_time - init_time) * 100 // 1 / 100
        print("Hard waiting for topology data to be initialized...")
        time.sleep(0.25*len(bundle.modules))
        bundle.print_topology_map(True)
        print(f"Took {took} seconds to initialize")
        msg1 = parse_message(0x07, 0, bundle.modules[0].id)
        msg2 = parse_message(0x2A, 0, bundle.modules[0].id)
        print(f"sending request message... {msg1}")
        bundle._exe_thrd.close()
        init_time = time.perf_counter()
        bundle.send(msg1)
        bundle.send(msg2)
        while True:
            msg = bundle.recv()
            recv_cmd = decode_message(msg)[0] if msg else None
            if msg and recv_cmd == 0x07:
                break
        fin_time = time.perf_counter()
        took = fin_time - init_time
        print(f"received message... {msg}")
        print(f"Took {took / 2:.10f} seconds for message transfer")
        os._exit(0)

    # Update STM32 modules (every modules but network module)
    if check_option('-u', '--update'):
        init_time = time.time()
        updater = STM32FirmwareUpdater()
        updater.update_module_firmware()
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
            module_name = type(module).__name__.lower()
            print(">>> " + module_name + " = bundle." + module_name + "s[0]")
            exec(module_name + " = module")

    # Run GUI debugger
    if check_option('-g', '--gui'):
        print(">>> bundle = modi.MODI()")
        init_time = time.time()
        from modi.debugger import Debugger
        bundle = Debugger()
        fin_time = time.time()
        print(f'Took {fin_time - init_time:.2f} seconds to init MODI modules')
        for module in bundle.modules:
            module_name = type(module).__name__.lower()
            print(">>> " + module_name + " = bundle." + module_name + "s[0]")
            exec(module_name + " = module")
