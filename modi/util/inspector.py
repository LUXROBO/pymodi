import os
import time

from textwrap import fill
from textwrap import dedent


class Inspector:
    """
    Inspector diagnoses malfunctioning STM32 modules (all modules but network)
    """

    row_len = 79

    def __init__(self):
        self.bundle = None

    @staticmethod
    def clear():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        os.system(clear_cmd)

    def print_wrap(self, msg):
        message = fill(dedent(msg), self.row_len).lstrip()
        print(message)

    def print_module_page(self, module, i, nb_modules):
        print('-' * self.row_len)
        module_to_inspect = f"| Diagnosing {module.module_type} ({module.id})"
        progress = f"({i+1} / {nb_modules}) |"
        s = f"{module_to_inspect:<{self.row_len}}"
        s = progress.join(s.rsplit(' '*len(progress), 1))
        print(s)
        print('-' * self.row_len)

    def inspect(self, module, i, nb_modules):
        self.print_module_page(module, i, nb_modules)

        inspect_module = {
            # inspection method for input modules
            "button": self.inspect_button,
            "dial": self.inspect_dial,
            "env": self.inspect_env,
            "gyro": self.inspect_gyro,
            "ir": self.inspect_ir,
            "mic": self.inspect_mic,
            "ultrasound": self.inspect_ultrasound,

            # inspection method for input modules
            "display": self.inspect_display,
            "led": self.inspect_led,
            "motor": self.inspect_motor,
            "speaker": self.inspect_speaker,
        }.get(module.module_type)
        inspect_module(module)

        self.clear()

    def inspect_button(self, button):
        pass

    def inspect_dial(self, dial):
        pass

    def inspect_env(self, env):
        pass

    def inspect_gyro(self, gyro):
        pass

    def inspect_ir(self, ir):
        pass

    def inspect_mic(self, mic):
        pass

    def inspect_ultrasound(self, ultrasound):
        pass

    def inspect_display(self, display):
        pass

    def inspect_led(self, led):
        pass

    def inspect_motor(self, motor):
        pass

    def inspect_speaker(self, speaker):
        pass

    #
    # Main methods are defined below
    #
    def run_inspection(self):
        self.clear()
        print("=" * self.row_len)
        print(f"= {'This is PyMODI Module Inspector':^{self.row_len - 4}} =")
        print("=" * self.row_len)

        self.print_wrap(
            """
            PyMODI provides a number of tools that can be utilized in different
            purpose. One of them is the STM32 module (all modules but network)
            inspector which diagnoses any malfunctioning MODI module.
            """
        )

        nb_modules = int(input(dedent(
            """
            Connect network module to your local machine, attach other modi
            modules to the network module. When attaching modi modules, make
            sure that you provide sufficient power to the modules. Using modi
            battery module is a good way of supplying the power to the modules.

            Type the number of modi modules (integer value) that are connected
            to the network module (note that the maximum number of modules is
            20) and press ENTER:
            """.rstrip() + " "
        )))
        self.clear()

        if not (1 <= nb_modules <= 20):
            print(f"ERROR: {nb_modules} is invalid for the number of modules")
            os._exit(0)

        print("Importing modi package and creating a modi bundle object...\n")
        import modi
        self.bundle = modi.MODI()

        stm32_modules = \
            [m for m in self.bundle.modules if m.module_type != "Network"]
        nb_modules_detected = len(stm32_modules)
        if nb_modules != nb_modules_detected:
            self.print_wrap(
                f"""
                You said that you have attached {nb_modules} modules but PyMODI
                detects only {nb_modules_detected} number of modules! Look at
                the printed log above regarding module connection and check
                which modules have not been printed above.
                """
            )
            os._exit(0)

        input(dedent(
            """
            It looks like all stm modules have been initialized properly! Let's
            diagnose each module, one by one!

            press ENTER to continue:
            """.rstrip() + " "
        ))
        self.clear()

        # Let's inspect each stm module!
        for i, module in enumerate(stm32_modules):
            self.inspect(module, i, nb_modules)
