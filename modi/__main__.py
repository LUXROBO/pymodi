import os
import sys
import time
import textwrap

from getopt import getopt, GetoptError

import modi

from modi.util.usage import Usage
from modi.util.tutor import Tutor


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
            sys.argv[1:], "tihu",
            [
                "tutorial",
                "initialize",
                "help",
                "usage",
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

    # Initialize modules implicitly
    if check_option('-a', '--initialize'):
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

    # Show each module usage
    if check_option('-u', '--usage'):
        usage = Usage()
        usage.run_usage_manual()
        os._exit(0)
